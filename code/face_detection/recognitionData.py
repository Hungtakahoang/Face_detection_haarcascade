import cv2
import numpy as np
import os
import sqlite3
from PIL import Image
from SerialModule import SerialObject
import time


# time variances
cTime = 0
pTime = 0

# khởi tạo liên kết thông qua cổng com 
arduino = SerialObject()

# tạo hình ảnh 
imageON = cv2.imread("../img/light_bulb.png")
imageOFF = cv2.imread("../img/light_bulb_off.png")

# pre precessing image
percent_scale = 0.5
width = int(imageON.shape[1]*percent_scale)
height = int(imageON.shape[0]*percent_scale)
dim = (width, height)
imageON = cv2.resize(imageON,dim)
imageOFF = cv2.resize(imageOFF,dim)

# training hình ảnh nhận diện với thư viện khuôn mặt
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(r'D:\opencv-master\face_detection\recognizer\trainingData.yml')
# r'D:\opencv-master\face_detection\recognizer\trainingData.yml'

# tạo hàm lấy thông tin người từ database của mình (truy cập database lấy ID của người)
def getProfile(id):

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor = conn.execute("CREATE TABLE IF NOT EXISTS people (ID INTEGER NOT NULL, Names TEXT NOT NULL, PRIMARY KEY(ID))")
    # print("Create table_sqlite done")

    query = "SELECT * FROM people WHERE ID=" + str(id)
    cursor = conn.execute(query)

    profile = None

    for row in cursor:
        profile = row

    conn.close()
    return profile

# mở cam
cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_COMPLEX

while(True):
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces: 

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roi_gray = gray[y: y + h, x: x + w]

        # hàm predict sẽ trả về id và độ chính xác
        id, accuracy = recognizer.predict(roi_gray)

        # dùng hàm id để gọi getProfile để lấy thông tin hiển thị trên ảnh
        if accuracy < 50:
            profile = getProfile(id)
        
            # hàm putText dùng đề in kí tự trên màng hình, là một hàm trong thư viện opencv-python
            if(profile != None):
                cv2.putText(frame, ""+str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'ACC:{int(100 - accuracy)}%', (410, 100), fontface, 0.7, (0, 255, 0), 1)
                arduino.sendData([1])
                cv2.imshow('Graphic', imageON)

        else:
            cv2.putText(frame, "Unknow", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)
            cv2.putText(frame, f'ACC:{int(100 - accuracy)}%', (410, 100), fontface, 0.7, (0, 255, 0), 1)
            arduino.sendData([0])
            cv2.imshow('Graphic', imageOFF)

    # show fps:
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime 
    cv2.putText(frame, f'FSP:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

    cv2.imshow('frame_recognizer',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        arduino.sendData([0])
        cv2.imshow('Graphic', imageOFF)
        break

cap.release()
cv2.destroyAllWindows()
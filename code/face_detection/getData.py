import cv2
import numpy as np
import sqlite3
import os

def insertOrUpdate(id, name):
    # kết nối với đường dẫn của database vừa tạo
    conn = sqlite3.connect('data.db')

    # tạo bảng trong SQLite
    cursor = conn.cursor()
    cursor = conn.execute("CREATE TABLE IF NOT EXISTS people (ID INTEGER NOT NULL, Names TEXT NOT NULL, PRIMARY KEY(ID))")
    print("Create table_sqlite done")

    # Kiểm tra ID nhập vào đã tồn tại chưa, nếu rồi thì update nếu chưa thì insert
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cursor = conn.execute(query)

    isRecordExist = 0 #biến để kiểm tra có tồn tại ID trước đó chưa

    for row in cursor:
        isRecordExist = 1

    if(isRecordExist == 0):
        query = "INSERT INTO people(ID, Names) VALUES("+str(id)+ ", '"+str(name)+"')"

    else: 
        query = "UPDATE people SET Names='"+str(name)+"' WHERE ID="+str(id)
    
    conn.execute(query)
    conn.commit()
    conn.close()

insertOrUpdate(1,'Hung')

#load tv
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

#insert to database
id = input("Enter your ID: ")
name = input("Enter your Name: ")

insertOrUpdate(id, name)

simpleNum = 0

while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        simpleNum += 1 
        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(simpleNum)+'.jpg', gray[y: y + h, x: x + w])
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if simpleNum > 100:
        break

cap.release()
cv2.destroyAllWindows()
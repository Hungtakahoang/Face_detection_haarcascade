import cv2
import numpy as np
import os
from PIL import Image

# tải thư viện opencv-contrib-python để dùng được câu lệnh dưới đây
recognizer = cv2.face.LBPHFaceRecognizer_create()

path = 'dataSet' #path là dẫn đến thư mục chưa ảnh database của mình vừa tạo

def getImageWithId(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # os.listdir là lệnh đưa đến tất cả các lệnh trong thư mục

    #print(imagePaths)
    faces = [] # mảng để lưu dữ liệu ảnh
    IDs = [] # mảng để lưu ID của các ảnh

    # duyệt tất cả đường dẫn, rồi convert về PIL 
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L') # L chính là grayscale

        # chuyển faceImg chuyển về array để train
        faceNp = np.array(faceImg, 'uint8')
        
        #print(faceNp)

        # lấy ID dùng split để cắt
        # tên ảnh là 'dataSet\\User.1.1.jpg', cắt từ dấu \\ dataSet là phần tử 0, User.1.1.jpg là phần tử 1
        # là lấy phần tử 1 rồi cắt từ dấu chấm rồi tiếp tục lấy phần tử 1 sẽ lấy ra đúng Id
        Id = int(imagePath.split('\\')[1].split('.')[1])
        
        # rồi gán vào 2 biến faces và IDs
        faces.append(faceNp)
        IDs.append(Id)

        cv2.imshow('training', faceNp)
        cv2.waitKey(10)
    
    return faces, IDs

faces, Ids = getImageWithId(path) # để lưu vào

# thực hiện train
recognizer.train(faces, np.array(Ids))

# tạo file với định dạng file.yml
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainingData.yml')

cv2.destroyAllWindows()
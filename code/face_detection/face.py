import cv2
# trích suất ảnh từ camera
cap = cv2.VideoCapture(0)
# load model haarcascade
detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while (True):
    ret, img = cap.read()
    # chuyển về ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # nhận diện khuôn mặt
    face = detect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in face:
        # vẽ 1 đường bao quanh khuôn mặt
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    # hiển thị ảnh nhận diện
    cv2.imshow('DETECTING FACE', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
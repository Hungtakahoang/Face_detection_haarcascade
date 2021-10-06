import cv2
import mediapipe as mp 
import time 

cTime = 0
pTime = 0
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection = 0, min_detection_confidence = 0.5
) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print('ignoring empty camera frame')
            continue
        
        #image.flags.writeable = False

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        result = face_detection.process(image)

        #image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if result.detections:
            for id, detection in enumerate(result.detections):
                # cách 1
                # mp_drawing.draw_detection(image, detection)
                # cách 2
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = image.shape
                #bboxC.ymin = bboxC.ymin + 10
                bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih), int(bboxC.width*iw), int(bboxC.height*ih)
                cv2.rectangle(image, bbox, (255, 0, 255), 2)
                cv2.putText(image, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow('FaceDetection', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
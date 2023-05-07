import threading

import cv2
from deepface import DeepFace


url = "http://192.168.1.8:8080/video"

# cap = cv2.VideoCapture(url)
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

reference_img = cv2.imread("abdul.jpg")  # use your own image here

face_match = False


def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False


while True:
    ret, frame = cap.read()

    
    if counter % 30 == 0:
        try:
            threading.Thread(target=check_face, args=(frame.copy(),)).start()
        except ValueError:
            pass
    counter += 1
    if face_match:
        cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    else:
        cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()

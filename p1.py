import cv2
import face_recognition
img = cv2.imread("abdul.jpg")
rbg_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rbg_img)[0]

url = "http://192.168.82.26:8080/video"
# cap = cv2.VideoCapture(url)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Mobile Camera Stream", frame)
    result = face_recognition.compare_faces([img_encoding],frame)
    client_socket.send(str("u").encode())
    print(result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import face_recognition
img = cv2.imread("abdul.jpg")
rbg_img = cv2.cvtColor(img,cv2.COLORBGR2RGB)
img_encoding = face_recognition.face_encodings(rbg_img)[0]

result = face_recognition.compare_faces([img_encoding])
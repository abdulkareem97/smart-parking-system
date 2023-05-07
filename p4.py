import cv2
import face_recognition
import numpy as np
import socket
import time
HOST = '192.168.99.5'  # NodeMCU IP address
PORT = 80              # NodeMCU port number
# MESSAGE = 'Hello NodeMCU!'

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the NodeMCU server
client_socket.connect((HOST, PORT))
image_path = 'abdul.jpg'
image = face_recognition.load_image_file(image_path)
face_encoding = face_recognition.face_encodings(image)[0]

# Add face encoding and name to lists
known_face_encodings = [face_encoding]
known_face_names = ['Abdul']
video_capture = cv2.VideoCapture(0)
prev_name = 'Abdul'
name = 'Abdul'
# video_capture = cv2.VideoCapture('http://192.168.82.26:8080/video')
# print("here")
while True:
    # print("here3")

    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    
    # detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    # print("here4")


    # loop over each face
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # compare to known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        # prev_name = name
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]
            prev_name = name

        # draw box and label
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)
       
        
    # show frame
    cv2.imshow('Video', frame)
    if(prev_name !=name and name=='Unknown'):

        try:
            print("ProtoType : message will send to Abdul (ALert Somebody Else Is Driving Your Car)")
            prev_name = 'Unknown'
            client_socket.send(str(5).encode())
        except Exception as e:
            print("Error sending data:", e)
    # else:
    #     print(prev_name)
    
    # exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
print("here2")

video_capture.release()
cv2.destroyAllWindows()

import cv2
import matplotlib.pyplot as plt
import pyttsx3
import socket
import time
HOST = '192.168.99.5'  # NodeMCU IP address
PORT = 80              # NodeMCU port number
# MESSAGE = 'Hello NodeMCU!'

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the NodeMCU server
client_socket.connect((HOST, PORT))




engine = pyttsx3.init()
config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt.txt'
frozen_model = 'frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model,config_file)
model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)
text = ""
onLight = 1
prev = 0


# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('http://192.168.99.76:8080/video')
while True:
    ret,frame = cap.read()
    # rgb_frame = frame[:, :, ::-1]
    index,confidence,box = model.detect(frame,confThreshold=0.5)
    if len(index)!=0 and (1 in index):

        onLight = 1
        for student,conf,boxes in zip(index.flatten(),confidence.flatten(),box):
            if(student==1):
                
                print(student)
                cv2.rectangle(frame,boxes,(255,0,0),2)
    elif onLight:
        text = 'turn of ligth'
        print('turn of ligth')
        onLight = 0
        engine.say(text)
        engine.runAndWait()
            # send the message to the NodeMCU
       
    else:
        print("nothing")
    if(prev!=onLight):
        try:
            
            client_socket.send(str(onLight).encode())
        except Exception as e:
            print("Error sending data:", e)
    prev = onLight


    
    



        
  


    cv2.imshow('Smart Parking System',frame)
    if cv2.waitKey(2) and 0xFF == ord('q'):
        break


# close the socket
client_socket.close()
cap.release()
cv2.destroyAllWindows()
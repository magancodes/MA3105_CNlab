import cv2
import socket
import numpy as np
import time
import math


SERVER_IP = "127.0.0.1"   
SERVER_PORT = 5000
ADDR = (SERVER_IP, SERVER_PORT)
CHUNK_SIZE = 4096        
FPS = 20                  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


cap = cv2.VideoCapture("sample.mp4")  

if not cap.isOpened():
    print("Error: Cannot open video source")
    exit()

print("Server started, streaming video...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video stream")
        break

  
    frame = cv2.resize(frame, (400, 300))

   
    _, encoded_frame = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    data = encoded_frame.tobytes()

 
    num_chunks = math.ceil(len(data) / CHUNK_SIZE)

    for i in range(num_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk_data = data[start:end]

       
        marker = 1 if i == num_chunks - 1 else 0
        packet = bytes([marker]) + chunk_data
        server_socket.sendto(packet, ADDR)

    
    time.sleep(1 / FPS)

cap.release()
server_socket.close()

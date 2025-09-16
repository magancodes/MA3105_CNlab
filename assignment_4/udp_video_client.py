import cv2
import socket
import numpy as np


CLIENT_IP = "0.0.0.0"  
CLIENT_PORT = 5000
ADDR = (CLIENT_IP, CLIENT_PORT)
CHUNK_SIZE = 4096

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(ADDR)

print("Client listening for video stream...")

buffer = b""

while True:
    packet, _ = client_socket.recvfrom(CHUNK_SIZE + 1)

    marker = packet[0]     
    data = packet[1:]      
    buffer += data

    if marker == 1:  
        
        frame = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("UDP Video Client", frame)

        buffer = b"" 

    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

client_socket.close()
cv2.destroyAllWindows()

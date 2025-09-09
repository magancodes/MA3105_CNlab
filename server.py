import socket
import threading

SERVER_NAME = "Server of magancodes"
SERVER_INT = 42
HOST = "0.0.0.0"
PORT = 6000

def handle_client(conn, addr):
    print(f"[+] Connected with {addr}")
    try:
        data = conn.recv(1024).decode()
        if not data:
            return
        client_name, client_num = data.split(",")
        client_num = int(client_num)
        if not (1 <= client_num <= 100):
            print("Invalid number received. Terminating server...")
            conn.close()
            exit(0)
        print("\n=== Received from client ===")
        print(f"Client Name: {client_name}")
        print(f"Server Name: {SERVER_NAME}")
        print(f"Client Integer: {client_num}")
        print(f"Server Integer: {SERVER_INT}")
        print(f"Sum: {client_num + SERVER_INT}\n")
        response = f"{SERVER_NAME},{SERVER_INT}"
        conn.sendall(response.encode())
    finally:
        conn.close()
        print(f"[-] Connection with {addr} closed")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[SERVER] Listening on {HOST}:{PORT} ...")
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()

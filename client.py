import socket

CLIENT_NAME = "Client of magancodes"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000

def main():
    while True:
        try:
            num = int(input("Enter an integer between 1 and 100: "))
            if 1 <= num <= 100:
                break
            else:
                print("Number must be between 1 and 100.")
        except ValueError:
            print("Please enter a valid integer.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        message = f"{CLIENT_NAME},{num}"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024).decode()
        server_name, server_num = data.split(",")
        server_num = int(server_num)
        print("\n=== Received from server ===")
        print(f"Client Name: {CLIENT_NAME}")
        print(f"Server Name: {server_name}")
        print(f"Client Integer: {num}")
        print(f"Server Integer: {server_num}")
        print(f"Sum: {num + server_num}\n")

if __name__ == "__main__":
    main()

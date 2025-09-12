import socket

HOST = "127.0.0.1"   
PORT = 8081         

def handle_request(request):
   
    headers = request.split("\r\n")
    cookie_header = None
    for header in headers:
        if header.startswith("Cookie:"):
            cookie_header = header
            break

    if not cookie_header:
        response_body = """
        <html>
            <head><title>Cookie Demo</title></head>
            <body style="font-family:Arial; text-align:center; padding:50px; background:#f0f8ff;">
                <h1>Welcome, New User!</h1>
                <p>A cookie has been set for you. Refresh the page to see the effect.</p>
            </body>
        </html>
        """
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Set-Cookie: user=User123; Path=/; Max-Age=3600\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "\r\n"
        )
        return response_headers + response_body

    else:
        cookie_value = cookie_header.split("=", 1)[1]
        response_body = f"""
        <html>
            <head><title>Cookie Demo</title></head>
            <body style="font-family:Arial; text-align:center; padding:50px; background:#fff0f5;">
                <h1>Welcome back, {cookie_value}!</h1>
                <p>You already have a cookie stored on your browser.</p>
            </body>
        </html>
        """
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "\r\n"
        )
        return response_headers + response_body


def start_server():
  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"🚀 Cookie Server running at http://{HOST}:{PORT}")

        while True:
            client_conn, client_addr = server_socket.accept()
            with client_conn:
                request = client_conn.recv(1024).decode("utf-8")
                if not request:
                    continue

                print("📥 Incoming request:")
                print(request.split("\r\n\r\n")[0]) 

                response = handle_request(request)

                client_conn.sendall(response.encode("utf-8"))
                print("📤 Response sent\n")


if __name__ == "__main__":
    start_server()

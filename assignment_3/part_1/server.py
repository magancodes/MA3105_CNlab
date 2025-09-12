import http.server
import socketserver
import hashlib
import os
import email.utils

PORT = 8080
FILE_TO_SERVE = "index.html"

class CachingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = FILE_TO_SERVE

        # Ensure file exists
        if not os.path.exists(self.path):
            self.send_error(404, "File not found")
            print(f"[404] {self.path} not found")
            return

        # --- Generate ETag (MD5 hash of file content) ---
        with open(self.path, "rb") as f:
            file_content = f.read()
            etag = hashlib.md5(file_content).hexdigest()

        # --- Last-Modified header (file modification time) ---
        last_modified_time = os.path.getmtime(self.path)
        last_modified_str = email.utils.formatdate(last_modified_time, usegmt=True)

        # --- Check request headers ---
        if_none_match = self.headers.get("If-None-Match")
        if_modified_since = self.headers.get("If-Modified-Since")

        # Strong validator: ETag
        if if_none_match == etag:
            self.send_response(304)
            self.end_headers()
            print(f"[304 Not Modified] Path: {self.path} | Matched ETag: {etag}")
            return

        # Weak validator: Last-Modified
        if if_modified_since:
            try:
                since_time = email.utils.parsedate_to_datetime(if_modified_since).timestamp()
                if int(since_time) >= int(last_modified_time):
                    self.send_response(304)
                    self.end_headers()
                    print(f"[304 Not Modified] Path: {self.path} | Matched Last-Modified: {last_modified_str}")
                    return
            except Exception:
                pass  # Ignore parsing errors, serve normally

        # --- Otherwise, send the file with headers ---
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified_str)
        self.end_headers()
        self.wfile.write(file_content)

        # Print response details
        print(f"[200 OK] Path: {self.path}")
        print(f" → ETag: {etag}")
        print(f" → Last-Modified: {last_modified_str}")
        print(f" → Content-Length: {len(file_content)} bytes\n")


# Run server
with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT} (http://localhost:{PORT}/)")
    httpd.serve_forever()

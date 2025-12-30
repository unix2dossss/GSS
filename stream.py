import cv2
import time
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class Streamer:
    def __init__(self, host="0.0.0.0", port=7070):
        self.frame = None
        streamer = self  # closure for handler

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                return

            def do_GET(self):
                if self.path == "/" or self.path == "/index.html":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    self.wfile.write(
                        b"""<!doctype html>
<html>
  <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body style="margin:0;background:#000;display:flex;justify-content:center;align-items:center;height:100vh;">
    <img src="/stream" style="max-width:100%;max-height:100%;" />
  </body>
</html>"""
                    )
                    return

                if self.path != "/stream":
                    self.send_response(404)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header("Age", "0")
                self.send_header("Cache-Control", "no-cache, private")
                self.send_header("Pragma", "no-cache")
                self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
                self.end_headers()

                try:
                    while True:
                        if streamer.frame is None:
                            time.sleep(0.01)
                            continue

                        ok, jpeg = cv2.imencode(".jpg", streamer.frame)
                        if not ok:
                            time.sleep(0.01)
                            continue

                        data = jpeg.tobytes()

                        self.wfile.write(b"--frame\r\n")
                        self.wfile.write(b"Content-Type: image/jpeg\r\n")
                        self.wfile.write(f"Content-Length: {len(data)}\r\n\r\n".encode())
                        self.wfile.write(data)
                        self.wfile.write(b"\r\n")
                        self.wfile.flush()

                        time.sleep(1 / 15)
                except (BrokenPipeError, ConnectionResetError, socket.error):
                    return

        self.server = ThreadingHTTPServer((host, port), Handler)
        print(f"[STREAM] http://{host}:{port}  (open / in browser)")
        import threading
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def on_frame(self, frame):
        self.frame = frame

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
# streamer.py
import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer

class Streamer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.frame = None

        streamer = self  # closure for handler

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != "/":
                    self.send_response(404)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header(
                    "Content-Type", "multipart/x-mixed-replace; boundary=frame"
                )
                self.end_headers()

                while True:
                    if streamer.frame is None:
                        continue

                    ret, jpeg = cv2.imencode(".jpg", streamer.frame)
                    if not ret:
                        continue

                    self.wfile.write(b"--frame\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(jpeg)))
                    self.end_headers()
                    self.wfile.write(jpeg.tobytes())
                    self.wfile.write(b"\r\n")

        self.server = HTTPServer((host, port), Handler)
        print(f"[STREAM] http://{host}:{port}")

        # run server in background thread
        import threading
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def on_frame(self, frame):
        self.frame = frame

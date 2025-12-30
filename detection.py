from datetime import datetime
from notification import notify, send_photo
import numpy as np
import cv2
import os
import time

class Detector:
    def __init__(self, pixel_diff_thresh=10, area_thresh=8000):
        self._prev_frame = None
        self._frame_count = 0
        self.MOVEMENT_THRESHOLD = 0.5

        self.pixel_diff_thresh = pixel_diff_thresh
        self.area_thresh = area_thresh

        self._detected_motion = False
        self._recording_in_progress = False

        self._frame_recording_count = 0
        self._out = None

        self._timestamp = None

    def preprocess(self, frame, first=False):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)

        if first and self._prev_frame is None:
            self._prev_frame = blurred

        return blurred
    
    def setup_recording(self):
        self._recording_in_progress = True

        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")


        now = datetime.now()
        self._timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        self._out = cv2.VideoWriter(f'/home/unix2dos/GarageSecuritySystem/garage_recordings/{self._timestamp}.mp4', fourcc, 30, (640, 480))

    def cleanup_recording(self):
            self._detected_motion = False
            self._recording_in_progress = False
            self._frame_recording_count=0

            self._out.release()
            self._out = None

    def send_snapshot_notif(self, frame):
        snapshot_path = f"snapshots/motion_{int(time.time())}.jpg"
        os.makedirs("snapshots", exist_ok=True)

        cv2.imwrite(snapshot_path, frame)
        send_photo(snapshot_path, caption="Garage Activity Snapshot.")

    def on_frame(self, frame):
        self._frame_count += 1
        if self._prev_frame is None:
            self.preprocess(frame, first=True)
            return

        current_frame = self.preprocess(frame)

        diff = cv2.absdiff(self._prev_frame, current_frame)
        _, mask = cv2.threshold(diff, self.pixel_diff_thresh, 255, cv2.THRESH_BINARY)

        mask = cv2.dilate(mask, None, iterations=2)

        motion_area = int(np.sum(mask > 0))

        if motion_area > self.area_thresh and self._frame_count > 10*30:
            self._detected_motion = True

        if self._detected_motion and not self._recording_in_progress:
            print("Significant movement detected!")
            print("recording started")
            notify("Motion detected! Recording in progress.")
            self.setup_recording()
        
        if self._recording_in_progress:
            self._out.write(frame)

            if self._frame_recording_count == 30*30:
                self.send_snapshot_notif(frame)

            self._frame_recording_count += 1

        self._prev_frame = current_frame

        # cv2.imshow("Preview", current_frame)

        if self._frame_recording_count == 60*30:
            print("recording stopped")
            notify(f'Recording complete. Motion event saved. Check http://100.115.208.89:8088/{self._timestamp}.mp4')
            self.cleanup_recording()

        cv2.waitKey(1)
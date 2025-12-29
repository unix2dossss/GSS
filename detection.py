from datetime import datetime
import numpy as np
import cv2

class Detector:
    def __init__(self, pixel_diff_thresh=25, area_thresh=1000):
        self._prev_frame = None
        self._frame_count = 0
        self.MOVEMENT_THRESHOLD = 0.5

        self.pixel_diff_thresh = pixel_diff_thresh
        self.area_thresh = area_thresh

        self._detected_motion = False
        self._recording_in_progress = False

        self._frame_recording_count = 0
        self._out = None

    def preprocess(self, frame, first=False):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)

        if first and self._prev_frame is None:
            self._prev_frame = blurred

        return blurred
    
    def setup_recording(self):
        self._recording_in_progress = True

        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        self._out = cv2.VideoWriter(f'{timestamp}.avi', fourcc, 30, (640, 480))

    def cleanup_recording(self):
            self._detected_motion = False
            self._recording_in_progress = False
            self._frame_recording_count=0

            self._out.release()
            self._out = None

    def on_frame(self, frame):
        if self._prev_frame is None:
            self.preprocess(frame, first=True)
            return

        current_frame = self.preprocess(frame)

        diff = cv2.absdiff(self._prev_frame, current_frame)
        _, mask = cv2.threshold(diff, self.pixel_diff_thresh, 255, cv2.THRESH_BINARY)

        mask = cv2.dilate(mask, None, iterations=2)

        motion_area = int(np.sum(mask > 0))

        if motion_area > self.area_thresh:
            self._detected_motion = True
            print("Significant movement detected!")
            print("Changed pixels:", motion_area)

        if self._detected_motion and not self._recording_in_progress:
            print("recording started")
            self.setup_recording()
        
        if self._recording_in_progress:
            self._out.write(frame)
            self._frame_recording_count += 1

        self._prev_frame = current_frame

        cv2.imshow("Preview", current_frame)

        if self._frame_recording_count==10*30:
            print("recording stopped")
            self.cleanup_recording()

        cv2.waitKey(1)
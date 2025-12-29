import cv2

class Detector:
    def __init__(self):
        pass

    def on_frame(self, frame):
        cv2.imshow("Preview", frame)
        cv2.waitKey(1)
import cv2

def run(bus, camera_index):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError("Could not open camera")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            bus.publish("frame", frame)

    finally:
        cap.release()

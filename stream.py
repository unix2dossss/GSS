class Streamer:
    def __init__(self):
        pass

    def on_frame(self, frame):
        print(frame.shape)
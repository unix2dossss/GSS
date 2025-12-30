# main.py

from pubsub.broker import EventBus
from frame import run
from detection import Detector
from stream import Streamer

bus = EventBus()

detector = Detector()
streamer = Streamer()

bus.subscribe("frame", detector.on_frame)
bus.subscribe("frame", streamer.on_frame)

try:
    run(bus, 2)
finally:
    streamer.stop()
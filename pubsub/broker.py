# pubsub/broker.py

class EventBus:
    def __init__(self):
        self._subs = {}  # event -> [handlers]

    def subscribe(self, event: str, handler):
        self._subs.setdefault(event, []).append(handler)

    def publish(self, event: str, data):
        for handler in self._subs.get(event, []):
            handler(data)

class EventBus:
    def __init__(self):
        # A dictionary to map event names to a list of functions waiting for them
        self._subscribers = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def emit(self, event_type: str, data):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)


# Create a global instance (singleton) for simplicity
event_bus = EventBus()

from collections import defaultdict
from loguru import logger
from .singleton import SingletonMeta


class EventBus(metaclass=SingletonMeta):
    def __init__(self):
        self.listeners = defaultdict(list)
        logger.info("EventBus initialized.")

    def subscribe(self, event_type: str, callback):
        """Subscribe a callback to an event type."""
        self.listeners[event_type].append(callback)
        logger.debug(
            f"Subscribed {getattr(callback, '__name__', 'callback')} to event '{event_type}'"
        )

    def publish(self, event_type: str, *args, **kwargs):
        """Publish an event to all subscribed callbacks."""
        logger.debug(f"Publishing event '{event_type}'")
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"Error calling callback for event '{event_type}': {e}"
                    )


event_bus = EventBus()

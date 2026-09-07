from collections import defaultdict
from typing import Callable, Type


class EventBus:
    """
    Lightweight in-process event bus.

    RabbitMQ can replace this adapter later without
    changing domain logic.
    """

    def __init__(self):

        self._handlers = defaultdict(list)

    def subscribe(
        self,
        event_type: Type,
        handler: Callable
    ):

        self._handlers[event_type].append(handler)

    def publish(self, event):

        event_type = type(event)

        for handler in self._handlers[event_type]:
            handler(event)

from collections import defaultdict
from threading import Lock
from typing import Any, Callable, DefaultDict

from loguru import logger

Callback = Callable[[Any], None]


class EventManager:
    def __init__(self, skip_topic_log:set[str]|None=None) -> None:
        self.skip_topic_log: set[str] = skip_topic_log if skip_topic_log else set()
        self.inscriptions: DefaultDict[str, list[Callback]] = defaultdict(list)
        self._lock = Lock()

    def publish(self, topic: str, message: Any = None) -> None:
        """Publish message to a topic

        Args:
            message (Any): A object to be passed as message
            topic (str): A topic to publish the object to
        """
        if topic not in self.skip_topic_log:
            logger.debug(f"[{topic}] {message}")
            
        with self._lock:
            topic_callbacks = self.inscriptions[topic]

        for callback in topic_callbacks:
            callback(message)

    def subscribe(self, topic: str, callback: Callback) -> None:
        """Subscribe a callable to a topic

        Args:
            callback (Callback): a callable to be called when something is posted to the topic
            topic (str): the topic to link the callback to
        """
        with self._lock:
            self.inscriptions[topic].append(callback)

    def subscribers(self, topic: str) -> list:
        """Retrive subscribers of a given topic

        Args:
            topic (str): topic name

        Returns:
            list: callbacks subscribed to topic
        """
        return self.inscriptions[topic]

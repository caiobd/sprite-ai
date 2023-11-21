from typing import Any

from pytest import fixture

from pet.event_manager import EventManager


@fixture
def event_manager():
    return EventManager()


def test_subscribe_single_callback(event_manager):
    topic = "test"

    def callback(event: Any):
        pass

    event_manager.subscribe(topic, callback)
    subscribers = event_manager.subscribers(topic)

    assert subscribers == [callback]


def test_subscribe_multiple_callbacks(event_manager):
    topic = "test"

    def callback1(event: Any):
        pass

    def callback2(event: Any):
        pass

    event_manager.subscribe(topic, callback1)
    event_manager.subscribe(topic, callback2)
    subscribers = event_manager.subscribers(topic)

    assert subscribers == [callback1, callback2]


def test_subscribers_no_subscriber(event_manager):
    topic = "test"
    subscribers = event_manager.subscribers(topic)

    assert subscribers == []


def test_publish_single_callback(event_manager):
    topic = "test"
    generic_list = []

    def callback(event: Any):
        generic_list.append("element")

    event_manager.subscribe(topic, callback)
    event_manager.publish(topic)

    assert generic_list == ["element"]


def test_publish_multiple_callbacks(event_manager):
    topic = "test"
    generic_list = []

    def callback1(event: Any):
        generic_list.append("element1")

    def callback2(event: Any):
        generic_list.append("element2")

    event_manager.subscribe(topic, callback1)
    event_manager.subscribe(topic, callback2)
    event_manager.publish(topic)

    assert generic_list == ["element1", "element2"]

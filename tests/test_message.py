from dataclasses import FrozenInstanceError

import pytest

from notifykit import Message, Severity


def test_defaults():
    message = Message(title="标题", text="正文")
    assert message.severity is Severity.INFO
    assert message.fields == {}
    assert message.url is None


def test_rejects_blank_title():
    with pytest.raises(ValueError):
        Message(title="  ", text="正文")


def test_rejects_blank_text():
    with pytest.raises(ValueError):
        Message(title="标题", text="\n")


def test_is_frozen():
    message = Message(title="标题", text="正文")
    with pytest.raises(FrozenInstanceError):
        message.title = "别的"  # type: ignore[misc]

"""四个 SDK 通道的薄壳：用假 SDK 断言我们传对了参数。"""

from __future__ import annotations

import importlib
import json
from types import SimpleNamespace

import pytest

from notifykit import Message, NotifyError
from notifykit.render.discord_embed import embed
from notifykit.render.feishu_card import card
from notifykit.render.slack_blocks import blocks
from notifykit.render.telegram_html import html

message = Message(title="标题", text="正文", fields={"交易所": "binance"}, url="http://h/")


async def test_feishu_bot_builds_request(monkeypatch):
    module = importlib.import_module("notifykit.channels.feishu_bot")
    captured = {}

    class FakeResource:
        def create(self, request):
            captured["request"] = request
            return SimpleNamespace(
                success=lambda: True, code=0, msg="ok", data=SimpleNamespace(message_id="om_1")
            )

    client = SimpleNamespace(im=SimpleNamespace(v1=SimpleNamespace(message=FakeResource())))
    channel = module.FeishuBot("cli_x", "secret", "oc_x", client=client)
    result = await channel.send(message)

    request = captured["request"]
    assert request.queries == [("receive_id_type", "chat_id")]
    assert request.body.receive_id == "oc_x"
    assert request.body.msg_type == "interactive"
    assert json.loads(request.body.content) == card(message)
    assert result.message_id == "om_1"


async def test_feishu_bot_rejection_raises():
    module = importlib.import_module("notifykit.channels.feishu_bot")

    class FakeResource:
        def create(self, request):
            return SimpleNamespace(
                success=lambda: False, code=230002, msg="bot not in chat", data=None
            )

    client = SimpleNamespace(im=SimpleNamespace(v1=SimpleNamespace(message=FakeResource())))
    channel = module.FeishuBot("cli_x", "secret", "oc_x", client=client)
    with pytest.raises(NotifyError, match="230002"):
        await channel.send(message)


async def test_telegram_sends_html(monkeypatch):
    module = importlib.import_module("notifykit.channels.telegram")
    captured = {}

    class FakeBot:
        def __init__(self, token):
            captured["token"] = token

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return False

        async def send_message(self, **kwargs):
            captured["kwargs"] = kwargs
            return SimpleNamespace(message_id=42)

    monkeypatch.setattr(module, "Bot", FakeBot)
    channel = module.Telegram("123:abc", "-100", thread_id=7)
    result = await channel.send(message)

    assert captured["token"] == "123:abc"
    assert captured["kwargs"]["chat_id"] == "-100"
    assert captured["kwargs"]["parse_mode"] == "HTML"
    assert captured["kwargs"]["message_thread_id"] == 7
    assert captured["kwargs"]["text"] == html(message)
    assert result.message_id == "42"


async def test_slack_sends_blocks_and_text(monkeypatch):
    module = importlib.import_module("notifykit.channels.slack")
    captured = {}

    class FakeClient:
        def __init__(self, url):
            captured["url"] = url

        def send(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(status_code=200, body="ok")

    monkeypatch.setattr(module, "WebhookClient", FakeClient)
    result = await module.Slack("https://hooks.slack.com/x").send(message)

    assert captured["url"] == "https://hooks.slack.com/x"
    assert captured["blocks"] == blocks(message)
    assert captured["text"].startswith("标题")
    assert result.ok


async def test_slack_rejection_raises(monkeypatch):
    module = importlib.import_module("notifykit.channels.slack")

    class FakeClient:
        def __init__(self, url):
            pass

        def send(self, **kwargs):
            return SimpleNamespace(status_code=400, body="invalid_blocks")

    monkeypatch.setattr(module, "WebhookClient", FakeClient)
    with pytest.raises(NotifyError, match="400"):
        await module.Slack("https://hooks.slack.com/x").send(message)


async def test_discord_sends_embed(monkeypatch):
    module = importlib.import_module("notifykit.channels.discord")
    captured = {}

    class FakeWebhook:
        @classmethod
        def from_url(cls, url):
            captured["url"] = url
            return cls()

        def send(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(id=99)

    monkeypatch.setattr(module, "SyncWebhook", FakeWebhook)
    result = await module.Discord("https://discord.com/api/webhooks/x", username="哨塔").send(
        message
    )

    assert captured["url"] == "https://discord.com/api/webhooks/x"
    assert captured["embed"] == embed(message)
    assert captured["username"] == "哨塔"
    assert captured["wait"] is True
    assert result.message_id == "99"

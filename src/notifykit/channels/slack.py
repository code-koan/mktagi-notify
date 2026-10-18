"""Slack Incoming Webhook：用官方 ``slack-sdk`` 的 ``WebhookClient``。

webhook 只能发到它绑定的那个频道；要发别处得用 bot token，暂不支持。
"""

from __future__ import annotations

import asyncio
import time

try:
    from slack_sdk.webhook import WebhookClient
except ImportError as exc:  # pragma: no cover
    raise ImportError("Slack 需要官方 SDK：pip install 'notify-kit[slack]'") from exc

from notifykit.errors import NotifyError
from notifykit.message import Message
from notifykit.render.slack_blocks import blocks, fallback_text
from notifykit.result import DeliveryResult, elapsed_ms


class Slack:
    """``webhook_url`` 来自 Slack App 的 Incoming Webhooks。"""

    name = "slack"

    def __init__(self, webhook_url: str) -> None:
        self._url = webhook_url

    async def send(self, message: Message) -> DeliveryResult:
        client = WebhookClient(self._url)
        started = time.perf_counter()
        response = await asyncio.to_thread(
            client.send, text=fallback_text(message), blocks=blocks(message)
        )
        if response.status_code != 200:
            raise NotifyError(
                f"Slack 拒绝了消息：status={response.status_code} body={response.body}"
            )
        return DeliveryResult(channel=self.name, ok=True, latency_ms=elapsed_ms(started))

"""Telegram Bot：官方只有 HTTP API，用事实标准 ``python-telegram-bot``。

出站只需要 ``Bot``，不需要 ``Application``，也不会启动轮询。
"""

from __future__ import annotations

import time

try:
    from telegram import Bot
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Telegram 需要 python-telegram-bot：pip install 'notify-kit[telegram]'"
    ) from exc

from notifykit.message import Message
from notifykit.render.telegram_html import html
from notifykit.result import DeliveryResult, elapsed_ms


class Telegram:
    """``chat_id`` 可以是 ``-100...`` 的群，也可以是用户 id；话题用 ``thread_id``。"""

    name = "telegram"

    def __init__(self, token: str, chat_id: str, *, thread_id: int | None = None) -> None:
        self._token = token
        self._chat_id = chat_id
        self._thread_id = thread_id

    async def send(self, message: Message) -> DeliveryResult:
        started = time.perf_counter()
        async with Bot(self._token) as bot:
            sent = await bot.send_message(
                chat_id=self._chat_id,
                text=html(message),
                parse_mode="HTML",
                message_thread_id=self._thread_id,
            )
        return DeliveryResult(
            channel=self.name,
            ok=True,
            message_id=str(sent.message_id),
            latency_ms=elapsed_ms(started),
        )

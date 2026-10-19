"""Discord webhook：用 ``discord.py`` 的同步 ``SyncWebhook``，省掉 aiohttp 会话管理。"""

from __future__ import annotations

import asyncio
import time
from typing import Any, cast

try:
    from discord import SyncWebhook
except ImportError as exc:  # pragma: no cover
    raise ImportError("Discord 需要 discord.py：pip install 'mktagi-notify[discord]'") from exc

from mktagi_notify.message import Message
from mktagi_notify.render.discord_embed import embed
from mktagi_notify.result import DeliveryResult, elapsed_ms


class Discord:
    """``webhook_url`` 来自频道设置里的 Integrations → Webhooks。"""

    name = "discord"

    def __init__(self, webhook_url: str, *, username: str | None = None) -> None:
        self._url = webhook_url
        self._username = username

    async def send(self, message: Message) -> DeliveryResult:
        hook = SyncWebhook.from_url(self._url)
        started = time.perf_counter()
        # discord.py 的 send 是重载，放进 to_thread 时推不出参数，这里放宽类型
        send = cast(Any, hook.send)
        sent = await asyncio.to_thread(
            send, embed=embed(message), username=self._username, wait=True
        )
        message_id = str(getattr(sent, "id", "") or "")
        return DeliveryResult(
            channel=self.name,
            ok=True,
            message_id=message_id or None,
            latency_ms=elapsed_ms(started),
        )

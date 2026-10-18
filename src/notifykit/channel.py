"""通道协议、并发分发、环境变量装配。"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterable, Sequence
from typing import Protocol, runtime_checkable

from notifykit.message import Message
from notifykit.result import DeliveryResult


@runtime_checkable
class Channel(Protocol):
    """一个通知通道。实现只需要一个属性加一个方法。"""

    name: str

    async def send(self, message: Message) -> DeliveryResult: ...


async def fanout(channels: Iterable[Channel], message: Message) -> list[DeliveryResult]:
    """并发发给所有通道，按传入顺序返回结果。

    单个通道失败不会影响其他通道，也不向外抛异常：失败信息在 ``error`` 里。
    """
    return list(await asyncio.gather(*(_deliver(channel, message) for channel in channels)))


async def _deliver(channel: Channel, message: Message) -> DeliveryResult:
    name = getattr(channel, "name", type(channel).__name__)
    try:
        return await channel.send(message)
    except Exception as exc:  # 兜住通道实现里的任何异常，避免一个通道带挂整轮
        return DeliveryResult(channel=name, ok=False, error=str(exc) or type(exc).__name__)


def from_env(prefix: str = "NOTIFYKIT_") -> list[Channel]:
    """按环境变量装配通道，凭据不全的通道直接跳过。

    变量名：``{prefix}FEISHU_WEBHOOK_URL``、``{prefix}FEISHU_WEBHOOK_SECRET``、
    ``{prefix}FEISHU_APP_ID``、``{prefix}FEISHU_APP_SECRET``、``{prefix}FEISHU_CHAT_ID``、
    ``{prefix}TELEGRAM_BOT_TOKEN``、``{prefix}TELEGRAM_CHAT_ID``、``{prefix}TELEGRAM_THREAD_ID``、
    ``{prefix}SLACK_WEBHOOK_URL``、``{prefix}DISCORD_WEBHOOK_URL``。
    """

    def get(key: str) -> str | None:
        return os.environ.get(prefix + key) or None

    channels: list[Channel] = []

    if url := get("FEISHU_WEBHOOK_URL"):
        from notifykit.channels import FeishuWebhook

        channels.append(FeishuWebhook(url, get("FEISHU_WEBHOOK_SECRET")))

    feishu_app = (get("FEISHU_APP_ID"), get("FEISHU_APP_SECRET"), get("FEISHU_CHAT_ID"))
    if all(feishu_app):
        from notifykit.channels import FeishuBot

        app_id, app_secret, chat_id = feishu_app
        channels.append(FeishuBot(str(app_id), str(app_secret), str(chat_id)))

    if (token := get("TELEGRAM_BOT_TOKEN")) and (chat_id := get("TELEGRAM_CHAT_ID")):
        from notifykit.channels import Telegram

        thread_id = get("TELEGRAM_THREAD_ID")
        channels.append(Telegram(token, chat_id, thread_id=int(thread_id) if thread_id else None))

    if url := get("SLACK_WEBHOOK_URL"):
        from notifykit.channels import Slack

        channels.append(Slack(url))

    if url := get("DISCORD_WEBHOOK_URL"):
        from notifykit.channels import Discord

        channels.append(Discord(url))

    return channels


def channel_names(channels: Sequence[Channel]) -> list[str]:
    """调试用：列出通道名。"""
    return [getattr(channel, "name", type(channel).__name__) for channel in channels]

"""飞书自定义机器人。

官方没有出 SDK，签名和投递按官方文档自己实现：把 ``"{timestamp}\\n{secret}"``
用 HMAC-SHA256 算摘要再 Base64，随 ``timestamp``、``sign`` 两个字段一起发。
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time

import httpx

from notifykit.errors import NotifyError
from notifykit.message import Message
from notifykit.render.feishu_card import card
from notifykit.result import DeliveryResult, elapsed_ms


def sign(secret: str, timestamp: int) -> str:
    """飞书自定义机器人的签名。"""
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


class FeishuWebhook:
    """群里「添加机器人」拿到的 webhook 地址。机器人开了签名校验才需要 secret。"""

    name = "feishu-webhook"

    def __init__(
        self,
        url: str,
        secret: str | None = None,
        *,
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._url = url
        self._secret = secret
        self._timeout = timeout
        self._transport = transport

    async def send(self, message: Message) -> DeliveryResult:
        payload: dict = {"msg_type": "interactive", "card": card(message)}
        if self._secret:
            timestamp = int(time.time())
            payload["timestamp"] = str(timestamp)
            payload["sign"] = sign(self._secret, timestamp)

        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(
                timeout=self._timeout, transport=self._transport
            ) as client:
                response = await client.post(self._url, json=payload)
        except httpx.HTTPError as exc:
            raise NotifyError(f"请求飞书失败：{exc}") from exc

        try:
            body = response.json()
        except ValueError as exc:
            raise NotifyError("飞书返回的不是 JSON") from exc

        if body.get("code") != 0:
            raise NotifyError(f"飞书拒绝了消息：code={body.get('code')} msg={body.get('msg')}")

        return DeliveryResult(channel=self.name, ok=True, latency_ms=elapsed_ms(started))

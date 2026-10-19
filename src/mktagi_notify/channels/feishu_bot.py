"""飞书应用机器人：用官方 ``lark-oapi`` 调 ``im/v1/messages``。

需要企业自建应用，应用要有「以应用身份发消息」的权限，并把机器人拉进目标群。
官方 SDK 是同步的，这里丢到线程里跑。
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any, cast

try:
    import lark_oapi as lark
    from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
except ImportError as exc:  # pragma: no cover - 只有没装 extra 时才会走到
    raise ImportError(
        "飞书应用机器人需要官方 SDK：pip install 'mktagi-notify[feishu-bot]'"
    ) from exc

from mktagi_notify.errors import NotifyError
from mktagi_notify.message import Message
from mktagi_notify.render.feishu_card import card
from mktagi_notify.result import DeliveryResult, elapsed_ms


class FeishuBot:
    """应用机器人。``chat_id`` 是要发进去的群。"""

    name = "feishu-bot"

    def __init__(
        self, app_id: str, app_secret: str, chat_id: str, *, client: lark.Client | None = None
    ) -> None:
        self._chat_id = chat_id
        self._client = client or (
            lark.Client.builder().app_id(app_id).app_secret(app_secret).build()
        )

    async def send(self, message: Message) -> DeliveryResult:
        request = (
            CreateMessageRequest.builder()
            .receive_id_type("chat_id")
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(self._chat_id)
                .msg_type("interactive")
                .content(json.dumps(card(message), ensure_ascii=False))
                .build()
            )
            .build()
        )

        started = time.perf_counter()
        # lark-oapi 的资源树是动态挂上去的，类型标注成 Optional，这里按运行期实际形状取
        resource = cast(Any, self._client).im.v1.message
        response = await asyncio.to_thread(resource.create, request)
        if not response.success():
            raise NotifyError(f"飞书拒绝了消息：code={response.code} msg={response.msg}")

        message_id = getattr(response.data, "message_id", None)
        return DeliveryResult(
            channel=self.name,
            ok=True,
            message_id=str(message_id) if message_id else None,
            latency_ms=elapsed_ms(started),
        )

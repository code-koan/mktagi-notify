"""Telegram 的 HTML 文本。上限 4096 字符。"""

from __future__ import annotations

from notifykit.message import Message
from notifykit.render.common import clip, to_telegram_html

LIMIT = 4096


def html(message: Message) -> str:
    parts = [
        f"<b>{to_telegram_html(message.title)}</b>",
        to_telegram_html(message.text),
    ]
    if message.fields:
        rows = [
            f"<b>{to_telegram_html(k)}</b>：{to_telegram_html(v)}"
            for k, v in message.fields.items()
        ]
        parts.append("\n".join(rows))
    if message.url:
        parts.append(message.url)
    return clip("\n\n".join(parts), LIMIT)

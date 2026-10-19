"""Discord embed。标题 256、描述 4096、字段值 1024、字段最多 25 个。"""

from __future__ import annotations

from mktagi_notify.message import Message, Severity
from mktagi_notify.render.common import clip

COLORS = {
    Severity.INFO: 0x3B82F6,
    Severity.SUCCESS: 0x22C55E,
    Severity.WARNING: 0xF59E0B,
    Severity.DANGER: 0xEF4444,
}


def embed(message: Message) -> dict:
    out: dict = {
        "title": clip(message.title, 256),
        "description": clip(message.text, 4096),
        "color": COLORS[message.severity],
    }
    if message.fields:
        out["fields"] = [
            {"name": clip(key, 256), "value": clip(value, 1024), "inline": True}
            for key, value in list(message.fields.items())[:25]
        ]
    if message.url:
        out["url"] = message.url
    return out

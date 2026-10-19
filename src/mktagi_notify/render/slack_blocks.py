"""Slack Block Kit。标题 150、单块 3000、字段最多 10 个。"""

from __future__ import annotations

from mktagi_notify.message import Message
from mktagi_notify.render.common import clip, to_slack_mrkdwn

TITLE_LIMIT = 150
SECTION_LIMIT = 2900
MAX_FIELDS = 10


def blocks(message: Message) -> list[dict]:
    out: list[dict] = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": clip(message.title, TITLE_LIMIT)},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": clip(to_slack_mrkdwn(message.text), SECTION_LIMIT)},
        },
    ]
    if message.fields:
        items = list(message.fields.items())[:MAX_FIELDS]
        out.append(
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": clip(f"*{key}*\n{value}", 2000)}
                    for key, value in items
                ],
            }
        )
    if message.url:
        out.append(
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"<{message.url}|查看详情>"}],
            }
        )
    return out


def fallback_text(message: Message) -> str:
    """通知栏和纯文本客户端看到的内容，Slack 要求带 text。"""
    return clip(f"{message.title}\n{message.text}", 3000)

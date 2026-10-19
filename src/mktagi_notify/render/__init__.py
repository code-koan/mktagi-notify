"""渲染器。纯函数，不碰网络，各自负责一种平台的载荷形状。"""

from __future__ import annotations

from mktagi_notify.render.common import clip, to_slack_mrkdwn, to_telegram_html
from mktagi_notify.render.discord_embed import embed
from mktagi_notify.render.feishu_card import card
from mktagi_notify.render.slack_blocks import blocks, fallback_text
from mktagi_notify.render.telegram_html import html

__all__ = [
    "blocks",
    "card",
    "clip",
    "embed",
    "fallback_text",
    "html",
    "to_slack_mrkdwn",
    "to_telegram_html",
]

"""渲染器。纯函数，不碰网络，各自负责一种平台的载荷形状。"""

from __future__ import annotations

from notifykit.render.common import clip, to_slack_mrkdwn, to_telegram_html
from notifykit.render.discord_embed import embed
from notifykit.render.feishu_card import card
from notifykit.render.slack_blocks import blocks, fallback_text
from notifykit.render.telegram_html import html

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

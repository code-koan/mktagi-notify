"""文本工具：截断与各通道的标记降级。"""

from __future__ import annotations

import html as _html
import re

ELLIPSIS = "…"
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)


def clip(text: str, limit: int) -> str:
    """超出上限就截断并加省略号。各平台的长度限制都是字符数。"""
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + ELLIPSIS


def to_telegram_html(text: str) -> str:
    """``**粗体**`` 转 Telegram 的 HTML 标记，同时转义 HTML 特殊字符。"""
    escaped = _html.escape(text, quote=False)
    return _BOLD.sub(r"<b>\1</b>", escaped)


def to_slack_mrkdwn(text: str) -> str:
    """``**粗体**`` 转 Slack 的 ``*粗体*``。"""
    return _BOLD.sub(r"*\1*", text)

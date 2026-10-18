"""飞书消息卡片 2.0。自定义机器人和应用机器人共用这一份对象。"""

from __future__ import annotations

from notifykit.message import Message, Severity

_TEMPLATES = {
    Severity.INFO: "blue",
    Severity.SUCCESS: "green",
    Severity.WARNING: "orange",
    Severity.DANGER: "red",
}


def card(message: Message) -> dict:
    """渲染成卡片对象。

    自定义机器人发的是 ``{"msg_type": "interactive", "card": <本对象>}``；
    应用机器人把本对象序列化成 ``content``。
    """
    elements: list[dict] = [{"tag": "markdown", "content": message.text}]
    if message.fields:
        lines = [f"**{key}**：{value}" for key, value in message.fields.items()]
        elements.append({"tag": "markdown", "content": "\n".join(lines)})
    if message.url:
        elements.append({"tag": "markdown", "content": f"[查看详情]({message.url})"})

    return {
        "schema": "2.0",
        "config": {"update_multi": True},
        "header": {
            "title": {"tag": "plain_text", "content": message.title},
            "template": _TEMPLATES[message.severity],
        },
        "body": {"elements": elements},
    }

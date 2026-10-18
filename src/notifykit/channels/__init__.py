"""五个通道。按需导入：只装了自己那个 extra 才 import 得动。

``from notifykit.channels import Telegram`` 在没装 extra 时会抛出带安装提示的
ImportError，而不是让整个包 import 失败。
"""

from __future__ import annotations

import importlib

_EXPORTS = {
    "FeishuWebhook": "notifykit.channels.feishu_webhook",
    "FeishuBot": "notifykit.channels.feishu_bot",
    "Telegram": "notifykit.channels.telegram",
    "Slack": "notifykit.channels.slack",
    "Discord": "notifykit.channels.discord",
}

# 名字由 __getattr__ 按需提供，pyright 看不到所以忽略这条
__all__ = ["FeishuWebhook", "FeishuBot", "Telegram", "Slack", "Discord"]  # pyright: ignore[reportUnsupportedDunderAll]


def __getattr__(name: str):
    module_path = _EXPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"notifykit.channels 没有 {name}")
    return getattr(importlib.import_module(module_path), name)


def __dir__() -> list[str]:
    return sorted(__all__)

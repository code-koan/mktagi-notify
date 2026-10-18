"""统一的消息通知包：飞书 webhook、飞书机器人、Telegram、Slack、Discord。

只导出六个名字，其余一律按需从子模块取。
"""

from __future__ import annotations

from notifykit.channel import Channel, channel_names, fanout, from_env
from notifykit.errors import ConfigError, NotifyError
from notifykit.message import Message, Severity
from notifykit.result import DeliveryResult

__version__ = "0.1.0"

__all__ = [
    "Channel",
    "ConfigError",
    "DeliveryResult",
    "Message",
    "NotifyError",
    "Severity",
    "__version__",
    "channel_names",
    "fanout",
    "from_env",
]

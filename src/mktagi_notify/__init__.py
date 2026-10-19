"""统一的消息通知包：飞书 webhook、飞书机器人、Telegram、Slack、Discord。

只导出六个名字，其余一律按需从子模块取。
"""

from __future__ import annotations

from mktagi_notify.channel import Channel, channel_names, fanout, from_env
from mktagi_notify.errors import ConfigError, NotifyError
from mktagi_notify.message import Message, Severity
from mktagi_notify.result import DeliveryResult

__version__ = "0.0.1"

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

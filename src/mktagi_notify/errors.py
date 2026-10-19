"""异常。通道内部抛这些，``fanout`` 负责转成 ``DeliveryResult``。"""

from __future__ import annotations


class NotifyError(RuntimeError):
    """发送失败：网络错误、平台拒绝、返回体不合法。"""


class ConfigError(NotifyError):
    """通道配置缺失或互相冲突。"""

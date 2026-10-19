"""发送结果。"""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    """一个通道的一次投递结果。失败时 ``error`` 有值，不抛异常。"""

    channel: str
    ok: bool
    message_id: str | None = None
    error: str | None = None
    latency_ms: int = 0

    def __bool__(self) -> bool:
        return self.ok


def elapsed_ms(started: float) -> int:
    """从 ``time.perf_counter()`` 的起点算毫秒。"""
    return int((time.perf_counter() - started) * 1000)

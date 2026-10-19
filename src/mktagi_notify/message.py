"""统一的消息模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    """消息严重程度。各通道把它映射成卡片颜色或图标。"""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


@dataclass(frozen=True, slots=True)
class Message:
    """一条要发出去的消息。

    字段刻意少：只保留五个通道都能表达的东西。图片、附件、@人、按钮交互
    各通道差异太大，不放进统一模型。

    ``text`` 里只允许一种标记：``**粗体**``，各通道渲染时自行降级。
    """

    title: str
    text: str
    fields: dict[str, str] = field(default_factory=dict)
    severity: Severity = Severity.INFO
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title 不能为空")
        if not self.text.strip():
            raise ValueError("text 不能为空")

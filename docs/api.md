# API

## 数据模型

```python
Message(title: str, text: str, fields: dict[str, str] = {}, severity: Severity = Severity.INFO, url: str | None = None)
```

- `title`、`text` 不能为空字符串或只有空白，否则构造时抛 `ValueError`。
- `text` 里只允许一种标记 `**粗体**`。
- 对象不可变（frozen dataclass）。

```python
Severity.INFO | Severity.SUCCESS | Severity.WARNING | Severity.DANGER
```

各通道把它映射成颜色：飞书卡片模板、Discord embed 颜色。Telegram 和 Slack 没有对应概念，忽略。

```python
DeliveryResult(channel: str, ok: bool, message_id: str | None = None, error: str | None = None, latency_ms: int = 0)
```

`bool(result)` 等于 `result.ok`。

## 通道

```python
class Channel(Protocol):
    name: str

    async def send(self, message: Message) -> DeliveryResult: ...
```

`isinstance(obj, Channel)` 可用（`runtime_checkable`），检查的是有没有 `name` 和 `send`。

## 并发分发

```python
results: list[DeliveryResult] = await fanout(channels, message)
```

- 并发发，按传入顺序返回。
- 任何一个通道抛异常都变成 `ok=False` 的结果，不向上抛。
- 空通道列表返回空列表。

## 环境变量装配

```python
channels = from_env(prefix="NOTIFYKIT_")
```

| 变量 | 需要一起给的 | 构建出的通道 |
| --- | --- | --- |
| `FEISHU_WEBHOOK_URL`（+ `FEISHU_WEBHOOK_SECRET` 可选） | — | `feishu-webhook` |
| `FEISHU_APP_ID` + `FEISHU_APP_SECRET` + `FEISHU_CHAT_ID` | 三个都要 | `feishu-bot` |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`（+ `TELEGRAM_THREAD_ID` 可选） | 两个都要 | `telegram` |
| `SLACK_WEBHOOK_URL` | — | `slack` |
| `DISCORD_WEBHOOK_URL` | — | `discord` |

凭据不全的通道直接跳过，不报错；一个都没配时返回空列表。前缀可换，方便同一台机器给多个应用配不同凭据。

## 渲染器

```python
from notifykit.render import card, html, embed, blocks, fallback_text
```

纯函数，输入 `Message`，输出该平台的载荷（dict / list / str）。可以脱离网络单独测，也是对接新平台时的扩展点。

## 版本

`notifykit.__version__` 与 `pyproject.toml` 的 `version` 必须一致（有测试守着），格式是 `X.Y.Z`。

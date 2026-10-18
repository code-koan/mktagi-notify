# notify-kit

一个消息发多个地方：飞书（自定义机器人 / 应用机器人）、Telegram、Slack、Discord。

核心只有三样东西：一个统一的消息模型、五个纯函数渲染器、五个通道薄壳。

```python
from notifykit import Message, Severity, fanout, from_env

results = await fanout(
    from_env(),
    Message(
        title="Q/USDT:USDT · 5 分钟急拉 3%",
        text="涨跌幅 **+5.39%**",
        fields={"交易所": "binanceusdm", "窗口": "最近 5 分钟"},
        severity=Severity.WARNING,
        url="http://applemini-mac:8848/",
    ),
)
```

## 安装

默认依赖只有 `httpx`。用哪个通道装哪个 extra：

```bash
pip install notify-kit                      # 只有飞书自定义机器人
pip install "notify-kit[feishu-bot]"        # 飞书应用机器人（官方 lark-oapi）
pip install "notify-kit[telegram]"          # Telegram（python-telegram-bot）
pip install "notify-kit[slack]"             # Slack（官方 slack-sdk）
pip install "notify-kit[discord]"           # Discord（discord.py）
pip install "notify-kit[all]"               # 全部
```

## 五个通道

| 通道 | 类 | 需要什么 | 卡片 | 回执 |
| --- | --- | --- | --- | --- |
| 飞书自定义机器人 | `FeishuWebhook` | webhook 地址，开了签名校验再加 secret | 消息卡片 2.0 | 无 |
| 飞书应用机器人 | `FeishuBot` | app_id、app_secret、chat_id | 同一份消息卡片 | message_id |
| Telegram | `Telegram` | bot token、chat_id（话题再加 thread_id） | 无卡片，标题加粗 | message_id |
| Slack | `Slack` | Incoming Webhook 地址 | Block Kit | 无 |
| Discord | `Discord` | webhook 地址 | embed | message_id |

每个通道的凭据来源、限制和未验证项写在 [docs/channels.md](docs/channels.md)。

## 约定

- **消息只有五个字段**：`title`、`text`、`fields`、`severity`、`url`。图片、附件、@人、按钮交互各平台差异太大，不进统一模型。
- **`text` 只认一种标记**：`**粗体**`。飞书原样发，Telegram 转 `<b>`，Slack 转 `*粗体*`，Discord 原样发。
- **发送不抛异常**：`fanout` 把任何通道的失败变成 `DeliveryResult(ok=False, error=...)`，一个通道挂了不影响其他通道。
- **渲染是纯函数**：`notifykit.render` 里没有网络，可以直接对 payload 做断言。
- **同步 SDK 丢线程**：`lark-oapi`、`slack-sdk`、`discord.SyncWebhook` 是同步的，适配器内部用 `asyncio.to_thread`，对外统一 `async`。

## 开发

```bash
uv sync --all-extras
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)，版本规则是 `X.Y.Z` 语义化版本，见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。

# 变更记录

格式沿用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号是 `X.Y.Z` 语义化版本：不兼容的改动升 X，新能力升 Y，修 bug 升 Z。

## [0.1.0] - 2026-10-18

### 新增

- `Message`、`Severity`、`DeliveryResult` 三个类型，`Channel` 协议，`fanout` 并发分发。
- 五个通道：`FeishuWebhook`（自定义机器人，自算签名）、`FeishuBot`（应用机器人，官方 `lark-oapi`）、`Telegram`（`python-telegram-bot`）、`Slack`（官方 `slack-sdk`）、`Discord`（`discord.py`）。
- `from_env()` 按环境变量装配通道，凭据不全的通道自动跳过。
- 四个纯函数渲染器：飞书卡片 2.0、Telegram HTML、Discord embed、Slack Block Kit。

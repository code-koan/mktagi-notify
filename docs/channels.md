# 通道配置与边界

## 飞书自定义机器人 `FeishuWebhook`

- 凭据：群设置 → 机器人 → 添加自定义机器人，拿到的 webhook 地址。开了「签名校验」再加 secret。
- 用的是消息卡片 2.0（`interactive`），`severity` 映射到卡片头部颜色：info 蓝、success 绿、warning 橙、danger 红。
- 官方没有 SDK，签名按[官方文档](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)自己实现：`HMAC-SHA256("{timestamp}\n{secret}", 空数据)` 再 Base64，随 `timestamp`、`sign` 字段发送。时间戳偏离当前时间超过 1 小时会被拒（code 19021）。
- 没有 message_id 回执，`DeliveryResult.message_id` 恒为 `None`。

## 飞书应用机器人 `FeishuBot`

- 凭据：企业自建应用的 app_id / app_secret，以及目标群的 chat_id。
- 需要应用开通「以应用身份发消息」权限，并把机器人拉进目标群；否则返回 230002 之类的错误码。
- 用官方 SDK `lark-oapi`，卡片对象与自定义机器人是同一份（`mktagi_notify.render.feishu_card.card`）。
- 未验证：`im/v1/messages` 的 `interactive` 消息里，`content` 直接放卡片对象是官方文档描述的形状，但我们只用假 SDK 测过参数，没有在真实应用上跑过。

## Telegram `Telegram`

- 凭据：@BotFather 拿的 token，以及 chat_id（群是负数，频道 `@name` 也行）。话题再给 `thread_id`。
- 用 `python-telegram-bot` 的 `Bot`，只发出站消息，不启动轮询。
- HTML 解析模式，`**粗体**` 转 `<b>`，正文里的 `<`、`>`、`&` 会转义。超过 4096 字符截断。
- 代理走环境变量（`HTTP_PROXY`/`HTTPS_PROXY`），包内不提供代理参数。

## Slack `Slack`

- 凭据：Slack App 的 Incoming Webhook 地址。
- 用官方 `slack-sdk` 的 `WebhookClient`，同时发 `text`（通知栏用）和 `blocks`（Block Kit）。
- webhook 只能发到它绑定的那个频道。要发多个频道或改消息，需要 bot token，暂不支持。

## Discord `Discord`

- 凭据：频道设置 → 整合 → Webhook 的地址。
- 用 `discord.py` 的 `SyncWebhook`（同步，内部 requests），省掉 aiohttp 会话管理。
- 发的是 embed：标题 256、描述 4096、字段值 1024、字段最多 25 个，超了截断。

## 共同的失败语义

- 平台拒绝（返回码非成功）：抛 `NotifyError`，消息里带平台给的 code / status，不带凭据。
- 网络错误、返回体不是 JSON：抛 `NotifyError`。
- `fanout` 把上述异常转成 `DeliveryResult(ok=False, error=...)`，不向上抛。

## 一个通道要多装什么

| 通道 | 需要装的 extra | 主依赖之外的库 |
| --- | --- | --- |
| 飞书自定义机器人 | 无 | 只需要 `httpx` |
| 飞书应用机器人 | `feishu-bot` | `lark-oapi` |
| Telegram | `telegram` | `python-telegram-bot`（LGPL-3.0） |
| Slack | `slack` | `slack-sdk` |
| Discord | `discord` | `discord.py` |

没装对应 extra 时，`from mktagi_notify.channels import Telegram` 会抛带安装提示的 `ImportError`，不影响其他通道。

# mktagi-notify

一个消息发多处：飞书（自定义机器人 / 应用机器人）、Telegram、Slack、Discord。

## 定位

可复用的 Python 库，不提供 CLI、不提供常驻服务、不做入站（不收消息）。
上层项目负责决定什么时候发、发什么；本包只负责把一条 `Message` 送到各平台。

## 目录

- `src/mktagi_notify/message.py`：唯一的数据模型，字段刻意少。
- `src/mktagi_notify/channel.py`：`Channel` 协议、`fanout`、`from_env`。
- `src/mktagi_notify/render/`：纯函数渲染器，不碰网络。
- `src/mktagi_notify/channels/`：五个适配器，各自一个文件，薄壳。
- `docs/`：通道配置与 API 说明，改行为时同批更新。

## 约束

- 默认依赖只有 `httpx`；每个平台 SDK 放在自己的 extra 里，不许进主依赖。
- 不手写 HTTP（飞书自定义机器人除外，官方没有 SDK）。
- 不自己实现重试、限流、模板引擎。SDK 有的用 SDK，没有的留给上层。
- 通道失败抛 `NotifyError`，由 `fanout` 转成 `DeliveryResult`，不允许吞掉。
- 版本号 `X.Y.Z`，`pyproject.toml` 与 `__init__.py` 两处一致，有测试守着。

## 命令

```bash
uv sync --all-extras
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

# 贡献指南

## 环境

需要 Python 3.10+ 和 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync --all-extras
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

四条全绿才算完成。CI 跑的是同样的命令，版本矩阵为 3.10 和 3.12。

## 提交

用 Conventional Commits，一句话说清改了什么：

```
feat: 新增 ntfy 通道
fix(telegram): 群话题 id 不再被强转成字符串
docs: 补飞书应用机器人的权限说明
```

## 提 PR

1. 先开 issue 说清场景，尤其是新通道——避免写完才发现不该加。
2. 一个 PR 只做一件事，带测试。
3. PR 描述里写「改了什么 / 为什么 / 怎么验证的」。
4. 检查清单：四条命令全绿、没有新增默认依赖、`CHANGELOG.md` 的 `Unreleased` 有一条。

## 新增一个通道

只加两个文件，别动别处：

1. `src/mktagi_notify/render/<平台>.py`：把 `Message` 变成该平台的 payload，纯函数，返回 dict / list / str。
2. `src/mktagi_notify/channels/<平台>.py`：一个类，`name` 属性 + `async def send(message) -> DeliveryResult`，内部用官方 SDK，同步 SDK 用 `asyncio.to_thread`。

然后补三处：`channels/__init__.py` 的 `_EXPORTS`、`channel.py` 的 `from_env`、`pyproject.toml` 里加一个 extra 并加进 `all`。

硬性要求：

- 不用 `requests`，不发手写 HTTP（本包唯一的例外是飞书自定义机器人，官方没有 SDK）。
- 失败抛 `NotifyError`，不要自己吞异常——`fanout` 负责兜。
- 渲染函数必须有单测断言真实 payload；通道适配器用假 SDK 测参数，不打真网络。

## 版本与发布

- 版本号写在 `pyproject.toml` 和 `src/mktagi_notify/__init__.py`，两处必须一致（有测试守着）。
- 当前处于 `0.0.x`：接口随时可能改，不要在生产里锁死小版本。到 `1.0.0` 才承诺兼容性。
- 发布由维护者做：改版本号 → 更新 `CHANGELOG.md` → 提交 → `git tag vX.Y.Z && git push --tags`。
- 打 tag 会触发 `.github/workflows/release.yml` 构建并创建 GitHub Release；Release 发布后由 `publish.yml` 用仓库 secret `PYPI_API_TOKEN` 发到 PyPI（同一个版本号只能发一次）。
- 手动发：`uv build` 然后 `UV_PUBLISH_TOKEN=... uv publish dist/*`。

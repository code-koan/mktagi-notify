## 改了什么

<!-- 一句话说清，例如：新增 ntfy 通道 -->

## 为什么

<!-- 关联 issue：fixes #123 -->

## 怎么验证的

<!-- 贴命令与结果；打了真网络的要说清发给谁、看没看到 -->

```
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run pyright
```

## 检查清单

- [ ] 四条命令全绿
- [ ] 新通道：渲染器有 payload 断言，适配器用假 SDK 测参数，没有新增主依赖
- [ ] `CHANGELOG.md` 的 `Unreleased` 加了一条
- [ ] 没有把 webhook、token、chat_id 提交进仓库

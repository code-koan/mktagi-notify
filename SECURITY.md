# 安全策略

## 报告漏洞

用 GitHub 的 [Private vulnerability reporting](https://github.com/code-koan/notify-kit/security/advisories/new) 提交，
不要开公开 issue。

请写清：受影响的版本、复现步骤、影响（比如能否让 webhook 把消息发到别处）、你已知的缓解办法。

维护者会在 7 天内答复，修复发布后在 advisory 里致谢（除非你要求匿名）。

## 凭据处理

- 本包不落盘、不缓存任何凭据，只在你构造通道时把字符串留在内存里。
- 报错信息里不会带上 webhook 地址和 token；`fanout` 返回的 `error` 只含平台给的原因。
- 提交 issue 或 PR 前，把 webhook、token、chat_id 换成占位符。

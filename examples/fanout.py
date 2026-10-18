"""一个消息发多处的例子。

凭据从环境变量读，没配的通道自动跳过：

    export NOTIFYKIT_FEISHU_WEBHOOK_URL=...
    export NOTIFYKIT_TELEGRAM_BOT_TOKEN=...
    export NOTIFYKIT_TELEGRAM_CHAT_ID=...
    python examples/fanout.py
"""

import asyncio

from notifykit import Message, Severity, channel_names, fanout, from_env


async def main() -> None:
    channels = from_env()
    if not channels:
        raise SystemExit("没有配置任何通道，先设置 NOTIFYKIT_* 环境变量")

    results = await fanout(
        channels,
        Message(
            title="Q/USDT:USDT · 5 分钟急拉 3%",
            text="涨跌幅 **+5.39%**",
            fields={"交易所": "binanceusdm", "对比窗口": "最近 5 分钟"},
            severity=Severity.WARNING,
            url="http://applemini-mac:8848/",
        ),
    )

    print("通道：", channel_names(channels))
    for result in results:
        state = "ok" if result.ok else f"失败：{result.error}"
        print(f"  {result.channel}: {state}")


if __name__ == "__main__":
    asyncio.run(main())

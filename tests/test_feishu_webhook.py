import httpx
import pytest

from notifykit import Message, NotifyError
from notifykit.channels.feishu_webhook import FeishuWebhook, sign
from notifykit.render.feishu_card import card


def _transport(handler):
    return httpx.MockTransport(handler)


def test_sign_matches_official_algorithm():
    # 官方文档的示例参数（secret="demo", timestamp=1599360473）
    assert sign("demo", 1599360473) == "l1N0gAcBjdwBvGm1xMjOF0XSyaLRpR7tuO5dHfhAYc8="


async def test_send_success_without_secret():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["payload"] = httpx.Response(200, content=request.content).json()
        return httpx.Response(200, json={"code": 0, "msg": "success"})

    channel = FeishuWebhook(
        "https://open.feishu.cn/open-apis/bot/v2/hook/x", transport=_transport(handler)
    )
    result = await channel.send(Message(title="t", text="x"))

    assert result.ok and result.channel == "feishu-webhook"
    assert seen["payload"]["card"] == card(Message(title="t", text="x"))
    assert "sign" not in seen["payload"]


async def test_send_adds_signature_when_secret_set():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = httpx.Response(200, content=request.content).json()
        assert payload["timestamp"].isdigit()
        assert payload["sign"] == sign("secret", int(payload["timestamp"]))
        return httpx.Response(200, json={"code": 0})

    channel = FeishuWebhook("https://example.invalid/hook", "secret", transport=_transport(handler))
    assert (await channel.send(Message(title="t", text="x"))).ok


async def test_platform_rejection_raises():
    channel = FeishuWebhook(
        "https://example.invalid/hook",
        transport=_transport(
            lambda request: httpx.Response(200, json={"code": 19021, "msg": "sign fail"})
        ),
    )
    with pytest.raises(NotifyError, match="19021"):
        await channel.send(Message(title="t", text="x"))


async def test_non_json_body_raises():
    channel = FeishuWebhook(
        "https://example.invalid/hook",
        transport=_transport(lambda request: httpx.Response(200, text="<html>")),
    )
    with pytest.raises(NotifyError, match="不是 JSON"):
        await channel.send(Message(title="t", text="x"))


async def test_network_error_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    channel = FeishuWebhook("https://example.invalid/hook", transport=_transport(handler))
    with pytest.raises(NotifyError, match="请求飞书失败"):
        await channel.send(Message(title="t", text="x"))

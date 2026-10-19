from mktagi_notify import Channel, DeliveryResult, Message, NotifyError, fanout

message = Message(title="t", text="x")


class Good:
    name = "good"

    async def send(self, message: Message) -> DeliveryResult:
        return DeliveryResult(channel=self.name, ok=True, message_id="1")


class Bad:
    name = "bad"

    async def send(self, message: Message) -> DeliveryResult:
        raise NotifyError("挂了")


async def test_results_keep_order_and_isolate_failure():
    results = await fanout([Bad(), Good()], message)
    assert [result.channel for result in results] == ["bad", "good"]
    assert results[0].ok is False
    assert "挂了" in (results[0].error or "")
    assert results[1].ok is True


async def test_empty_channels():
    assert await fanout([], message) == []


def test_channel_protocol_runtime_check():
    assert isinstance(Good(), Channel)
    assert not isinstance(object(), Channel)


def test_result_is_truthy_when_ok():
    assert DeliveryResult(channel="x", ok=True)
    assert not DeliveryResult(channel="x", ok=False)

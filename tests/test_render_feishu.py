from notifykit import Message, Severity
from notifykit.render.feishu_card import card


def test_card_shape():
    payload = card(Message(title="Q/USDT 急拉", text="涨跌幅 **+5.39%**"))
    assert payload["schema"] == "2.0"
    assert payload["header"]["title"]["content"] == "Q/USDT 急拉"
    assert payload["header"]["template"] == "blue"
    assert payload["body"]["elements"] == [{"tag": "markdown", "content": "涨跌幅 **+5.39%**"}]


def test_severity_template():
    for severity, template in [
        (Severity.INFO, "blue"),
        (Severity.SUCCESS, "green"),
        (Severity.WARNING, "orange"),
        (Severity.DANGER, "red"),
    ]:
        payload = card(Message(title="t", text="x", severity=severity))
        assert payload["header"]["template"] == template


def test_fields_and_url():
    payload = card(Message(title="t", text="x", fields={"交易所": "binance"}, url="http://h/"))
    contents = [element["content"] for element in payload["body"]["elements"]]
    assert "**交易所**：binance" in contents
    assert "[查看详情](http://h/)" in contents


def test_no_extra_elements_without_fields_or_url():
    payload = card(Message(title="t", text="x"))
    assert len(payload["body"]["elements"]) == 1

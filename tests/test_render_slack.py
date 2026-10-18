from notifykit import Message
from notifykit.render.slack_blocks import MAX_FIELDS, blocks, fallback_text


def test_blocks_shape():
    payload = blocks(Message(title="标题", text="涨跌幅 **+5.39%**"))
    assert payload[0]["type"] == "header"
    assert payload[0]["text"]["text"] == "标题"
    assert payload[1]["text"]["text"] == "涨跌幅 *+5.39%*"


def test_fields_capped():
    fields = {f"k{index}": "v" for index in range(MAX_FIELDS + 5)}
    payload = blocks(Message(title="t", text="x", fields=fields))
    section = next(block for block in payload if block.get("fields"))
    assert len(section["fields"]) == MAX_FIELDS


def test_url_becomes_context_link():
    payload = blocks(Message(title="t", text="x", url="http://h/"))
    assert payload[-1] == {
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": "<http://h/|查看详情>"}],
    }


def test_fallback_text_is_plain():
    text = fallback_text(Message(title="标题", text="正文"))
    assert text == "标题\n正文"

from mktagi_notify import Message, Severity
from mktagi_notify.render.discord_embed import COLORS, embed


def test_embed_shape():
    payload = embed(Message(title="标题", text="正文", severity=Severity.DANGER))
    assert payload["title"] == "标题"
    assert payload["description"] == "正文"
    assert payload["color"] == COLORS[Severity.DANGER]


def test_fields_capped_at_25():
    fields = {f"k{index}": "v" for index in range(30)}
    payload = embed(Message(title="t", text="x", fields=fields))
    assert len(payload["fields"]) == 25
    assert payload["fields"][0]["inline"] is True


def test_long_values_truncated():
    payload = embed(Message(title="t" * 300, text="x" * 5000))
    assert len(payload["title"]) == 256
    assert len(payload["description"]) == 4096


def test_url_and_no_fields_key():
    payload = embed(Message(title="t", text="x", url="http://h/"))
    assert payload["url"] == "http://h/"
    assert "fields" not in payload

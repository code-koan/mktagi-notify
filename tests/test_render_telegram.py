from mktagi_notify import Message
from mktagi_notify.render.telegram_html import LIMIT, html


def test_bold_becomes_b_tag():
    assert "<b>+5.39%</b>" in html(Message(title="t", text="涨跌幅 **+5.39%**"))


def test_html_is_escaped():
    assert "&lt;script&gt;" in html(Message(title="t", text="<script>"))


def test_title_is_bold_first_line():
    text = html(Message(title="标题", text="正文"))
    assert text.startswith("<b>标题</b>")


def test_fields_and_url():
    text = html(Message(title="t", text="x", fields={"窗口": "5 分钟"}, url="http://h/"))
    assert "<b>窗口</b>：5 分钟" in text
    assert "http://h/" in text


def test_truncated_to_limit():
    text = html(Message(title="t", text="x" * (LIMIT * 2)))
    assert len(text) == LIMIT
    assert text.endswith("…")

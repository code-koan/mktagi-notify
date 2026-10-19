from mktagi_notify import channel_names, from_env

VARS = {
    "FEISHU_WEBHOOK_URL": "https://open.feishu.cn/open-apis/bot/v2/hook/x",
    "FEISHU_WEBHOOK_SECRET": "secret",
    "FEISHU_APP_ID": "cli_x",
    "FEISHU_APP_SECRET": "app-secret",
    "FEISHU_CHAT_ID": "oc_x",
    "TELEGRAM_BOT_TOKEN": "123:abc",
    "TELEGRAM_CHAT_ID": "-100",
    "TELEGRAM_THREAD_ID": "7",
    "SLACK_WEBHOOK_URL": "https://hooks.slack.com/x",
    "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/x",
}


def _clear(monkeypatch):
    for key in VARS:
        monkeypatch.delenv(f"MKTAGI_NOTIFY_{key}", raising=False)


def test_no_env_means_no_channels(monkeypatch):
    _clear(monkeypatch)
    assert from_env() == []


def test_only_configured_channels_are_built(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MKTAGI_NOTIFY_FEISHU_WEBHOOK_URL", VARS["FEISHU_WEBHOOK_URL"])
    assert channel_names(from_env()) == ["feishu-webhook"]


def test_incomplete_credentials_are_skipped(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("MKTAGI_NOTIFY_TELEGRAM_BOT_TOKEN", "123:abc")
    monkeypatch.setenv("MKTAGI_NOTIFY_FEISHU_APP_ID", "cli_x")
    assert from_env() == []


def test_all_channels(monkeypatch):
    _clear(monkeypatch)
    for key, value in VARS.items():
        monkeypatch.setenv(f"MKTAGI_NOTIFY_{key}", value)
    assert channel_names(from_env()) == [
        "feishu-webhook",
        "feishu-bot",
        "telegram",
        "slack",
        "discord",
    ]


def test_custom_prefix(monkeypatch):
    monkeypatch.delenv("MYAPP_SLACK_WEBHOOK_URL", raising=False)
    monkeypatch.setenv("MYAPP_SLACK_WEBHOOK_URL", VARS["SLACK_WEBHOOK_URL"])
    assert channel_names(from_env(prefix="MYAPP_")) == ["slack"]

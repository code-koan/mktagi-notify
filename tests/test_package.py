import re
from pathlib import Path

import mktagi_notify

VERSION_LINE = re.compile(r'^version = "([^"]+)"', re.MULTILINE)

ROOT = Path(__file__).resolve().parents[1]


def test_version_matches_pyproject():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = VERSION_LINE.search(text)
    assert match is not None, "pyproject.toml 里没有 version 行"
    version = match.group(1)
    assert mktagi_notify.__version__ == version
    parts = version.split(".")
    assert len(parts) == 3, f"版本号必须是 X.Y.Z：{version}"
    assert all(part.isdigit() for part in parts)


def test_py_typed_marker_shipped():
    assert (ROOT / "src" / "mktagi_notify" / "py.typed").exists()


def test_public_api_is_small():
    assert sorted(mktagi_notify.__all__) == [
        "Channel",
        "ConfigError",
        "DeliveryResult",
        "Message",
        "NotifyError",
        "Severity",
        "__version__",
        "channel_names",
        "fanout",
        "from_env",
    ]

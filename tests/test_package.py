import re
from pathlib import Path

import notifykit

VERSION_LINE = re.compile(r'^version = "([^"]+)"', re.MULTILINE)

ROOT = Path(__file__).resolve().parents[1]


def test_version_matches_pyproject():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = VERSION_LINE.search(text)
    assert match is not None, "pyproject.toml 里没有 version 行"
    version = match.group(1)
    assert notifykit.__version__ == version
    parts = version.split(".")
    assert len(parts) == 3, f"版本号必须是 X.Y.Z：{version}"
    assert all(part.isdigit() for part in parts)


def test_py_typed_marker_shipped():
    assert (ROOT / "src" / "notifykit" / "py.typed").exists()


def test_public_api_is_small():
    assert sorted(notifykit.__all__) == [
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

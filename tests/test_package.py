from pathlib import Path

import tomllib

import notifykit

ROOT = Path(__file__).resolve().parents[1]


def test_version_matches_pyproject():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = metadata["project"]["version"]
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

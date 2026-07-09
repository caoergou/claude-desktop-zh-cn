# -*- coding: utf-8 -*-
"""Shared fixtures for claude-desktop-zh-cn tests."""

from __future__ import annotations

import json
import os
import struct
import sys
from pathlib import Path
from typing import Any

import pytest

# Make scripts/ importable as a module for tests.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

os.environ.setdefault("CLAUDE_ZH_RESOURCES_DIR", str(PROJECT_ROOT / "resources"))

import patch_claude_zh_cn as patcher  # noqa: E402


def align4(value: int) -> int:
    return value + ((4 - (value % 4)) % 4)


def _ensure_nested(node: dict[str, Any], part: str) -> dict[str, Any]:
    """Return the files dict for a directory node, creating it if needed."""
    if "files" not in node:
        node["files"] = {}
    return node["files"]


def _insert_file(header_files: dict[str, Any], parts: list[str], content: bytes, offset: int) -> None:
    """Insert a file entry into the nested header structure."""
    node: dict[str, Any] = {"files": header_files}
    for part in parts[:-1]:
        files = _ensure_nested(node, part)
        if part not in files:
            files[part] = {"files": {}}
        node = files[part]
    files = _ensure_nested(node, parts[-1])
    files[parts[-1]] = {
        "size": len(content),
        "offset": str(offset),
        "integrity": patcher.calculate_file_integrity(content),
    }


def build_asar_bytes(files: dict[str, bytes]) -> bytes:
    """Build a minimal valid app.asar archive for testing.

    Args:
        files: mapping from relative path (e.g. ".vite/build/index.js") to content.
    """
    header_files: dict[str, Any] = {}
    body = bytearray()

    for path, content in files.items():
        offset = len(body)
        body.extend(content)
        padding = align4(len(body)) - len(body)
        body.extend(b"\0" * padding)
        _insert_file(header_files, path.split("/"), content, offset)

    header = {"files": header_files}
    header_string = json.dumps(header, ensure_ascii=False, separators=(",", ":"))
    header_bytes = header_string.encode("utf-8")
    header_payload_size = align4(4 + len(header_bytes))
    header_pickle_size = 4 + header_payload_size

    header_pickle = bytearray(header_pickle_size)
    struct.pack_into("<I", header_pickle, 0, header_payload_size)
    struct.pack_into("<i", header_pickle, 4, len(header_bytes))
    header_pickle[8:8 + len(header_bytes)] = header_bytes

    result = bytearray()
    result.extend(struct.pack("<I", 4))
    result.extend(struct.pack("<I", header_pickle_size))
    result.extend(header_pickle)
    result.extend(body)
    return bytes(result)


@pytest.fixture
def build_asar_bytes_fixture() -> Any:
    return build_asar_bytes


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def fake_app(temp_dir: Path) -> Path:
    """Return a fake Claude.app directory with a valid app.asar inside."""
    app = temp_dir / "Claude.app"
    resources = app / "Contents" / "Resources"
    resources.mkdir(parents=True)

    asar_data = build_asar_bytes(
        {
            ".vite/build/index.js": b'console.log("hello");',
            ".vite/build/mainView.js": b'console.log("mainView");',
            ".vite/build/mainWindow.js": b'console.log("mainWindow");',
        }
    )
    (resources / "app.asar").write_bytes(asar_data)

    # Info.plist with ElectronAsarIntegrity so replace_asar_file_content can update it.
    plist = app / "Contents" / "Info.plist"
    import plistlib
    plist.parent.mkdir(parents=True, exist_ok=True)
    integrity = patcher.calculate_file_integrity(asar_data)
    plist.write_bytes(
        plistlib.dumps(
            {"ElectronAsarIntegrity": {"Resources/app.asar": integrity}},
            fmt=plistlib.FMT_XML,
        )
    )

    # Frontend i18n
    i18n = resources / "ion-dist" / "i18n"
    i18n.mkdir(parents=True)
    (i18n / "en-US.json").write_text(json.dumps({"hello": "Hello", "world": "World"}), encoding="utf-8")

    # Frontend assets
    assets = resources / "ion-dist" / "assets" / "v1"
    assets.mkdir(parents=True)
    (assets / "index-abc.js").write_text(
        'const LANGS=["en-US","de-DE","fr-FR","ko-KR","ja-JP","es-419","es-ES","it-IT","hi-IN","pt-BR","id-ID"];',
        encoding="utf-8",
    )

    return app


@pytest.fixture
def mock_resources(temp_dir: Path) -> Path:
    """Create a minimal resources directory for testing."""
    resources = temp_dir / "resources"
    resources.mkdir()

    for lang in ("zh-CN", "zh-TW", "zh-HK"):
        (resources / f"frontend-{lang}.json").write_text(
            json.dumps({"hello": "你好" if lang == "zh-CN" else "你好", "world": "世界"}, ensure_ascii=False),
            encoding="utf-8",
        )
        (resources / f"frontend-hardcoded-{lang}.json").write_text(
            json.dumps([["Search", "搜索" if lang == "zh-CN" else "搜尋"]], ensure_ascii=False),
            encoding="utf-8",
        )
        (resources / f"desktop-{lang}.json").write_text(
            json.dumps({"appName": "Claude"}, ensure_ascii=False),
            encoding="utf-8",
        )
        (resources / f"statsig-{lang}.json").write_text(
            json.dumps({"gate": "value"}, ensure_ascii=False),
            encoding="utf-8",
        )

    (resources / "Localizable.strings").write_text('"hello" = "你好";', encoding="utf-8")
    (resources / "manifest.json").write_text(
        json.dumps({"locale": "zh-CN", "name": "Chinese (Simplified)"}, ensure_ascii=False),
        encoding="utf-8",
    )
    (resources / "release.json").write_text(
        json.dumps({"repo": "javaht/claude-desktop-zh-cn", "release": "0.0.0"}, ensure_ascii=False),
        encoding="utf-8",
    )

    return resources


@pytest.fixture
def patcher_module() -> Any:
    return patcher

# -*- coding: utf-8 -*-
"""Tests for app.asar parsing and patching helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import patch_claude_zh_cn as patcher


class TestAsarHeaderRoundTrip:
    def test_build_and_read_header(self, patcher_module: Any, build_asar_bytes_fixture: Any, temp_dir: Path) -> None:
        data = build_asar_bytes_fixture({
            ".vite/build/index.js": b'console.log("hello");',
        })
        header_size, header_string, header = patcher_module.read_asar_header(data, Path("test.asar"))
        assert header_size > 0
        assert "files" in header
        assert ".vite" in header["files"]
        assert "build" in header["files"][".vite"]["files"]
        assert "index.js" in header["files"][".vite"]["files"]["build"]["files"]

    def test_encode_header_dynamic_matches_read(self, patcher_module: Any, build_asar_bytes_fixture: Any, temp_dir: Path) -> None:
        original = build_asar_bytes_fixture({
            ".vite/build/index.js": b'console.log("hello");',
        })
        header_size, header_string, header = patcher_module.read_asar_header(original, Path("test.asar"))

        encoded = patcher_module.encode_asar_header_dynamic(header_string)
        assert encoded[:4] == original[:4]  # size pickle payload == 4

        # Re-read header from encoded bytes plus dummy body.
        body = original[8 + header_size:]
        reassembled = encoded + body
        _, re_read, _ = patcher_module.read_asar_header(reassembled, Path("test.asar"))
        assert re_read == header_string


class TestAsarFileEntries:
    def test_get_file_entry(self, patcher_module: Any, build_asar_bytes_fixture: Any, temp_dir: Path) -> None:
        data = build_asar_bytes_fixture({
            ".vite/build/index.js": b'console.log("hello");',
            "nested/deep/file.txt": b'deep content',
        })
        _, _, header = patcher_module.read_asar_header(data, Path("test.asar"))

        entry = patcher_module.get_asar_file_entry(header, ".vite/build/index.js")
        assert entry["size"] == len(b'console.log("hello");')
        assert "integrity" in entry

        deep = patcher_module.get_asar_file_entry(header, "nested/deep/file.txt")
        assert deep["size"] == len(b"deep content")

    def test_iter_entries(self, patcher_module: Any, build_asar_bytes_fixture: Any, temp_dir: Path) -> None:
        data = build_asar_bytes_fixture({
            ".vite/build/index.js": b'a',
            "nested/deep/file.txt": b'b',
        })
        _, _, header = patcher_module.read_asar_header(data, Path("test.asar"))
        entries = patcher_module.iter_asar_file_entries(header)
        assert len(entries) == 2

    def test_missing_entry_raises(self, patcher_module: Any, build_asar_bytes_fixture: Any, temp_dir: Path) -> None:
        data = build_asar_bytes_fixture({".vite/build/index.js": b'a'})
        _, _, header = patcher_module.read_asar_header(data, Path("test.asar"))
        with pytest.raises(SystemExit):
            patcher_module.get_asar_file_entry(header, "missing.js")


class TestReplaceAsarFileContent:
    def test_replace_content_keeps_integrity(self, patcher_module: Any, fake_app: Path) -> None:
        asar_path = fake_app / "Contents" / "Resources" / "app.asar"
        new_content = b'console.log("patched");'

        changed = patcher_module.replace_asar_file_content(fake_app, ".vite/build/index.js", new_content)
        assert changed is True

        updated = asar_path.read_bytes()
        _, _, header = patcher_module.read_asar_header(updated, asar_path)
        entry = patcher_module.get_asar_file_entry(header, ".vite/build/index.js")
        assert entry["size"] == len(new_content)
        assert entry["integrity"]["hash"] == patcher_module.calculate_file_integrity(new_content)["hash"]

    def test_replace_same_content_returns_false(self, patcher_module: Any, fake_app: Path) -> None:
        asar_path = fake_app / "Contents" / "Resources" / "app.asar"
        original_data = asar_path.read_bytes()
        header_size, _, header = patcher_module.read_asar_header(original_data, asar_path)
        entry = patcher_module.get_asar_file_entry(header, ".vite/build/index.js")
        content_offset = 8 + header_size + int(entry["offset"])
        content_size = int(entry["size"])
        original_content = original_data[content_offset:content_offset + content_size]

        changed = patcher_module.replace_asar_file_content(fake_app, ".vite/build/index.js", original_content)
        assert changed is False

    def test_replace_changes_offsets(self, patcher_module: Any, fake_app: Path) -> None:
        asar_path = fake_app / "Contents" / "Resources" / "app.asar"
        original_data = asar_path.read_bytes()
        _, original_header_size, original_header = patcher_module.read_asar_header(original_data, asar_path)

        old_main_view = patcher_module.get_asar_file_entry(original_header, ".vite/build/mainView.js")
        old_main_view_offset = int(old_main_view["offset"])
        index_entry = patcher_module.get_asar_file_entry(original_header, ".vite/build/index.js")
        old_index_size = int(index_entry["size"])

        # Make index.js longer to shift subsequent files.
        new_index = b'console.log("this is a much longer replacement content");'
        patcher_module.replace_asar_file_content(fake_app, ".vite/build/index.js", new_index)

        updated_data = asar_path.read_bytes()
        _, _, updated_header = patcher_module.read_asar_header(updated_data, asar_path)
        new_main_view = patcher_module.get_asar_file_entry(updated_header, ".vite/build/mainView.js")
        delta = len(new_index) - old_index_size
        assert int(new_main_view["offset"]) == old_main_view_offset + delta


class TestCalculateFileIntegrity:
    def test_empty_data(self, patcher_module: Any) -> None:
        integrity = patcher_module.calculate_file_integrity(b"")
        assert integrity["algorithm"] == "SHA256"
        assert len(integrity["hash"]) == 64
        assert len(integrity["blocks"]) == 1

    def test_multi_block(self, patcher_module: Any) -> None:
        size = patcher_module.ASAR_INTEGRITY_BLOCK_SIZE + 1
        data = b"a" * size
        integrity = patcher_module.calculate_file_integrity(data)
        assert len(integrity["blocks"]) == 2

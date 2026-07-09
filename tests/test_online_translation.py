# -*- coding: utf-8 -*-
"""Tests for online claude.ai DOM translation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import patch_claude_zh_cn as patcher


class TestBuildOnlineTranslationMap:
    def test_basic_mapping(self, patcher_module: Any, fake_app: Path, mock_resources: Path, monkeypatch: Any) -> None:
        i18n = fake_app / "Contents" / "Resources" / "ion-dist" / "i18n"
        (i18n / "en-US.json").write_text(
            json.dumps({"hello": "Hello", "world": "World", "code": '{"foo":"bar"}'}, ensure_ascii=False),
            encoding="utf-8",
        )

        # Point patcher to mock resources (contains frontend-zh-CN.json).
        monkeypatch.setattr(patcher_module, "RESOURCES", mock_resources)

        mapping = patcher_module.build_online_translation_map(fake_app, "zh-CN")
        assert mapping["Hello"] == "你好"
        assert mapping["World"] == "世界"
        assert "{\"foo\":\"bar\"}" not in mapping.values()

    def test_ignores_identical_source_target(self, patcher_module: Any, fake_app: Path, mock_resources: Path, monkeypatch: Any) -> None:
        i18n = fake_app / "Contents" / "Resources" / "ion-dist" / "i18n"
        (i18n / "en-US.json").write_text(json.dumps({"same": "same"}, ensure_ascii=False), encoding="utf-8")

        # Use mock resources but override frontend-zh-CN.json with identical translation.
        (mock_resources / "frontend-zh-CN.json").write_text(
            json.dumps({"same": "same"}, ensure_ascii=False),
            encoding="utf-8",
        )
        monkeypatch.setattr(patcher_module, "RESOURCES", mock_resources)

        mapping = patcher_module.build_online_translation_map(fake_app, "zh-CN")
        assert "same" not in mapping


class TestBuildOnlineDomTranslationScript:
    def test_contains_language_marker(self, patcher_module: Any, fake_app: Path) -> None:
        mapping = {"Hello": "你好"}
        script = patcher_module.build_online_dom_translation_script("zh-CN", mapping)
        assert '"zh-CN"' in script
        assert '"Hello"' in script
        assert '"你好"' in script

    def test_dynamic_rules_for_zh_tw(self, patcher_module: Any, fake_app: Path) -> None:
        mapping = {}
        script = patcher_module.build_online_dom_translation_script("zh-TW", mapping)
        assert "已選擇" in script

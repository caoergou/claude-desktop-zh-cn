# -*- coding: utf-8 -*-
"""Tests for language whitelist patching."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import patch_claude_zh_cn as patcher


class TestLanguageWhitelistRegex:
    def test_matches_base_list(self, patcher_module: Any) -> None:
        text = 'const LANGS=["en-US","de-DE","fr-FR","ko-KR","ja-JP","es-419","es-ES","it-IT","hi-IN","pt-BR","id-ID"];'
        assert patcher_module.LANG_LIST_RE.search(text)

    def test_matches_list_with_zh_cn(self, patcher_module: Any) -> None:
        text = 'const LANGS=["en-US","de-DE","fr-FR","ko-KR","ja-JP","es-419","es-ES","it-IT","hi-IN","pt-BR","id-ID","zh-CN"];'
        assert patcher_module.LANG_LIST_RE.search(text)

    def test_matches_list_with_all_chinese(self, patcher_module: Any) -> None:
        text = 'const LANGS=["en-US","de-DE","fr-FR","ko-KR","ja-JP","es-419","es-ES","it-IT","hi-IN","pt-BR","id-ID","zh-CN","zh-TW","zh-HK"];'
        assert patcher_module.LANG_LIST_RE.search(text)

    def test_does_not_match_shortened_list(self, patcher_module: Any) -> None:
        text = 'const LANGS=["en-US","de-DE"];'
        assert patcher_module.LANG_LIST_RE.search(text) is None


class TestPatchLanguageWhitelist:
    def test_adds_zh_cn(self, patcher_module: Any, fake_app: Path) -> None:
        patcher_module.patch_language_whitelist(fake_app, "zh-CN")

        assets = fake_app / "Contents" / "Resources" / "ion-dist" / "assets" / "v1"
        text = (assets / "index-abc.js").read_text(encoding="utf-8")
        assert '"zh-CN"' in text

    def test_adds_zh_tw(self, patcher_module: Any, fake_app: Path) -> None:
        patcher_module.patch_language_whitelist(fake_app, "zh-TW")

        assets = fake_app / "Contents" / "Resources" / "ion-dist" / "assets" / "v1"
        text = (assets / "index-abc.js").read_text(encoding="utf-8")
        assert '"zh-TW"' in text

    def test_idempotent(self, patcher_module: Any, fake_app: Path) -> None:
        patcher_module.patch_language_whitelist(fake_app, "zh-CN")
        patcher_module.patch_language_whitelist(fake_app, "zh-CN")

        assets = fake_app / "Contents" / "Resources" / "ion-dist" / "assets" / "v1"
        text = (assets / "index-abc.js").read_text(encoding="utf-8")
        assert text.count('"zh-CN"') == 1

    def test_missing_bundle_raises(self, patcher_module: Any, fake_app: Path) -> None:
        assets = fake_app / "Contents" / "Resources" / "ion-dist" / "assets" / "v1"
        for js in assets.glob("*.js"):
            js.unlink()
        with pytest.raises(SystemExit):
            patcher_module.patch_language_whitelist(fake_app, "zh-CN")

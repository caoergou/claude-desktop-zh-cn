# -*- coding: utf-8 -*-
"""Tests for main-process menu patching helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import patch_claude_zh_cn as patcher


class TestBuildMenuRuntimePatch:
    def test_contains_label_and_role_maps(self, patcher_module: Any) -> None:
        script = patcher_module.build_menu_runtime_patch("zh-CN")
        assert patcher_module.MENU_RUNTIME_MARKER in script
        assert '"文件"' in script
        assert '"复制"' in script
        assert '"about"' in script

    def test_different_languages(self, patcher_module: Any) -> None:
        cn = patcher_module.build_menu_runtime_patch("zh-CN")
        tw = patcher_module.build_menu_runtime_patch("zh-TW")
        assert "檔案" in tw
        assert "文件" in cn


class TestReplaceMenuLiteralLengthPreserving:
    def test_preserves_byte_length(self, patcher_module: Any) -> None:
        text = 'const menu={label:"Open",role:"fileMenu"};'
        patched, count = patcher_module.replace_menu_literal_length_preserving(text, "Open", "开 ")
        assert count == 1
        assert len(patched.encode("utf-8")) == len(text.encode("utf-8"))
        assert 'label:"开 "' in patched

    def test_skips_when_target_too_long(self, patcher_module: Any) -> None:
        text = 'const menu={label:"File"};'
        patched, count = patcher_module.replace_menu_literal_length_preserving(text, "File", "这是一个很长的中文文本")
        # subn counts the match even when replacement is skipped to preserve length.
        assert patched == text
        assert 'label:"File"' in patched


class TestMainProcessMenuReplacements:
    def test_zh_cn_has_required_keys(self, patcher_module: Any) -> None:
        repl = patcher_module.get_main_process_menu_replacements("zh-CN")
        assert repl["File"] == "文件"
        assert repl["Settings…"] == "设置…"

    def test_role_replacements(self, patcher_module: Any) -> None:
        roles = patcher_module.get_main_process_menu_role_replacements("zh-CN")
        assert roles["quit"] == "退出"

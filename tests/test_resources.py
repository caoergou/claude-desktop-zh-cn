# -*- coding: utf-8 -*-
"""Tests that repository resource files are valid."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import patch_claude_zh_cn as patcher


class TestResourceJsonValidity:
    def test_all_resources_are_valid_json(self, patcher_module: Any) -> None:
        resources = patcher_module.RESOURCES
        json_files = list(resources.glob("*.json"))
        assert json_files, "No JSON files found in resources/"

        for path in json_files:
            data = json.loads(path.read_text(encoding="utf-8"))
            assert data is not None


class TestFrontendHardcodedShape:
    def test_hardcoded_files_are_string_pairs(self, patcher_module: Any) -> None:
        resources = patcher_module.RESOURCES
        for path in resources.glob("frontend-hardcoded-*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            assert isinstance(data, list), f"{path.name} should be a list"
            for index, item in enumerate(data):
                assert isinstance(item, list) and len(item) == 2, (
                    f"{path.name} item {index} should be a 2-element list"
                )
                assert isinstance(item[0], str), f"{path.name} item {index}[0] should be string"
                assert isinstance(item[1], str), f"{path.name} item {index}[1] should be string"


class TestManifestShape:
    def test_manifests_have_required_fields(self, patcher_module: Any) -> None:
        resources = patcher_module.RESOURCES
        for path in resources.glob("manifest*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            assert "language" in data, f"{path.name} missing language"
            assert "label" in data, f"{path.name} missing label"


class TestReleaseMetadata:
    def test_release_json_has_required_fields(self, patcher_module: Any) -> None:
        path = patcher_module.RESOURCES / "release.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "repo" in data
        assert "release" in data
        assert "/" in data["repo"]

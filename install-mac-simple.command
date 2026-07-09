#!/bin/bash
# Claude Desktop 中文补丁 - macOS 简易版
# 双击即安装：简体中文 + Cowork 兼容模式（最安全，不修改 app.asar）
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$TMP_DIR"

REPO="javaht/claude-desktop-zh-cn"
URL="https://github.com/${REPO}/releases/latest/download/claude-desktop-zh-cn-mac.zip"

echo "正在下载 Claude Desktop 中文补丁..."
curl -fsSL --retry 3 -o installer.zip "$URL" || {
  echo "下载失败，请检查网络连接。"
  exit 1
}

unzip -q installer.zip
cd claude-desktop-zh-cn-mac

export CLAUDE_ACTION=install
export CLAUDE_LANG=zh-CN
export CLAUDE_SKIP_ASAR_PATCH=1

exec ./install-mac.command

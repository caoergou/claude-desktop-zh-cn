#!/bin/bash
# 一键下载完整安装包并运行（macOS）
# 适合希望自主选择语言和模式的用户。

set -euo pipefail

REPO="javaht/claude-desktop-zh-cn"
VERSION="${CLAUDE_ZH_VERSION:-latest}"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$TMP_DIR"

if [ "$VERSION" = "latest" ]; then
  URL="https://github.com/${REPO}/releases/latest/download/claude-desktop-zh-cn-mac.zip"
else
  URL="https://github.com/${REPO}/releases/download/${VERSION}/claude-desktop-zh-cn-mac.zip"
fi

echo "正在下载 Claude Desktop 中文补丁（macOS）..."
curl -fsSL --retry 3 -o installer.zip "$URL" || {
  echo "下载失败，请检查网络或版本号是否正确。"
  exit 1
}

unzip -q installer.zip
cd claude-desktop-zh-cn-mac

if [ ! -x install-mac.command ]; then
  chmod +x install-mac.command
fi

# 启动交互式安装向导，让用户自主选择语言和模式。
exec ./install-mac.command "$@"

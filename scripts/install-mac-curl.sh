#!/bin/bash
# 一键下载并运行 Claude Desktop 中文补丁（macOS）
# 用法：
#   curl -fsSL https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-mac-curl.sh | bash
#   CLAUDE_ZH_VERSION=1.3.8 curl -fsSL ... | bash   # 安装指定版本

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

exec ./install-mac.command "$@"

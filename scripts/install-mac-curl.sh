#!/bin/bash
# 一键下载完整安装包并运行（macOS）
# 适合希望自主选择语言和模式的用户。
#
# 用法：
#   curl -fsSL https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-mac-curl.sh | bash
#
# 环境变量（可选，用于自动化）：
#   CLAUDE_ZH_VERSION=1.3.8     安装指定版本，默认 latest
#   CLAUDE_LANG=zh-CN           默认语言：zh-CN | zh-TW | zh-HK
#   CLAUDE_SKIP_ASAR_PATCH=1    1=Cowork 兼容模式，0=官方账号登录模式

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

# 如果用户通过环境变量指定了配置，则透传；否则进入交互式菜单。
if [ -n "${CLAUDE_LANG:-}" ] || [ -n "${CLAUDE_SKIP_ASAR_PATCH:-}" ]; then
  export CLAUDE_ACTION=install
  export CLAUDE_LANG="${CLAUDE_LANG:-zh-CN}"
  export CLAUDE_SKIP_ASAR_PATCH="${CLAUDE_SKIP_ASAR_PATCH:-1}"
fi

exec ./install-mac.command "$@"

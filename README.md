# Claude Desktop 中文补丁

[![CI](https://github.com/caoergou/claude-desktop-zh-cn/actions/workflows/ci.yml/badge.svg)](https://github.com/caoergou/claude-desktop-zh-cn/actions/workflows/ci.yml)
[![Latest Release](https://img.shields.io/github/v/release/caoergou/claude-desktop-zh-cn)](https://github.com/caoergou/claude-desktop-zh-cn/releases/latest)
[![GitHub Downloads](https://img.shields.io/github/downloads/caoergou/claude-desktop-zh-cn/total)](https://github.com/caoergou/claude-desktop-zh-cn/releases)

为 Claude Desktop 提供中文界面汉化，支持：

- 简体中文（`zh-CN`）
- 繁体中文（中国台湾，`zh-TW`）
- 繁体中文（中国香港，`zh-HK`）

支持 API 与官方订阅；如需使用第三方 API，请先参考 https://linux.do/topic/2032192 进行配置。

<img src="docs/images/claude-desktop-zh-cn-home.png" alt="Claude Desktop 中文界面截图" width="640">

---

## 目录

- [快速开始](#快速开始)
- [功能特点](#功能特点)
- [适用环境](#适用环境)
- [安装说明](#安装说明)
- [安装模式说明](#安装模式说明)
- [卸载 / 恢复](#卸载--恢复)
- [常见问题](#常见问题)
- [文件说明](#文件说明)
- [Star History](#star-history)
- [免责声明](#免责声明)

---

## 快速开始

### 第一步：下载安装脚本

前往 [Latest Release](https://github.com/caoergou/claude-desktop-zh-cn/releases/latest)，下载对应系统的文件：

| 系统 | 推荐下载 | 如何使用 |
| :--- | :--- | :--- |
| **macOS** | `install-mac-simple.command` | 双击运行 |
| **Windows** | `install-windows-simple.bat` | 右键 → **以管理员身份运行** |

> **推荐版**会默认安装：**简体中文 + Cowork 兼容模式**，全程无需选择，适合绝大多数用户。

### 第二步：等待完成

脚本会自动完成以下操作：

1. 尝试退出 Claude Desktop（如失败会提示你手动关闭）。
2. 下载并应用中文补丁。
3. 重启 Claude Desktop 并切换到简体中文。

整个过程一般只需几十秒。

### 需要其他语言或模式？

下载完整安装包 `claude-desktop-zh-cn-mac.zip` / `claude-desktop-zh-cn-windows.zip`，解压后运行：

- macOS：双击 `install-mac.command`
- Windows：右键 `install-windows.bat` → 以管理员身份运行

然后按提示选择语言和安装模式即可。

### 喜欢命令行？

<details>
<summary>点击展开命令行安装方式</summary>

命令行方式会下载**完整安装包**并启动安装向导，**可以自主选择语言和安装模式**。

#### macOS

```bash
curl -fsSL https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-mac-curl.sh | bash
```

#### Windows

在已打开的 PowerShell 窗口中运行：

```powershell
irm https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-windows-curl.ps1 | iex
```

或在 **cmd** / **Win + R** 中运行：

```cmd
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-windows-curl.ps1 | iex"
```

</details>

---

## 功能特点

- 支持三种中文变体：`zh-CN`、`zh-TW`、`zh-HK`。
- 自动将中文加入 Claude 前端语言白名单。
- macOS 自动合并当前 Claude 版本的 `en-US.json` 与中文翻译，新增未翻译字段保留英文。
- 提供 **Cowork 兼容模式**：不修改 `app.asar`，不破坏 Windows 签名。
- 提供 **官方账号登录模式**：在线 `claude.ai` 页面 DOM 翻译，聊天、项目、Artifacts 等显示中文。
- macOS 可绕过新版 Claude Desktop 对第三方 gateway 模型名的本地校验。
- 安装前自动备份，卸载时可一键恢复。
- 自动写入 Claude 用户配置，设置语言为所选中文变体。
- 支持同步 / 取消同步 CC Switch skills。
- 支持一键禁止 / 允许 Claude Desktop 自动更新。

---

## 适用环境

| 项目 | 要求 |
| :--- | :--- |
| 操作系统 | macOS 或 Windows |
| 前置软件 | 已安装 Claude Desktop |
| macOS 依赖 | 系统自带 Python 3（通常为 `/usr/bin/python3`） |
| Windows 依赖 | PowerShell，建议以管理员权限运行 |

---

## 安装说明

### 安装前

- 脚本会尝试自动退出 Claude Desktop；如果退出失败，请手动关闭（包括菜单栏 / 托盘图标）后再运行。
- 如需使用 **Cowork 沙箱 / 截图工作区**，请使用推荐版或手动选择 **Cowork 兼容模式**。

### macOS

1. 下载 `install-mac-simple.command`。
2. 双击运行。
3. 按提示输入 Mac 登录密码。
4. 等待 Claude 自动重启并切换为简体中文。

### Windows

1. 下载 `install-windows-simple.bat`。
2. 右键该文件 → **以管理员身份运行**。
3. 等待窗口提示完成。
4. Claude 会自动重启并切换为简体中文。

### 高级选项

<details>
<summary>需要选择语言或安装模式？点击展开</summary>

下载完整安装包并解压后运行：

- macOS：双击 `install-mac.command`
- Windows：右键 `install-windows.bat` → 以管理员身份运行

按菜单选择：

- `1` 安装中文补丁（官方账号登录模式）
- `2` 安装中文补丁（Cowork 兼容模式）
- `3` 恢复原样 / 卸载补丁
- `4` 禁止 / 允许自动更新
- `5` 同步 / 取消同步 CC Switch skills

然后选择语言：`1` 简体中文、`2` 繁体中文（中国台湾）、`3` 繁体中文（中国香港）。

</details>

---

## 安装模式说明

> 使用推荐版可以跳过本节，推荐版已默认使用 Cowork 兼容模式。

### Cowork 兼容模式

- **macOS 选项 `2` / Windows 模式 `1`**
- 不修改 `app.asar`，不会破坏 Windows 下 `Claude.exe` 的 Authenticode 签名。
- 适合需要使用 **Cowork 沙箱 / 截图工作区** 的用户。
- 第三方模型名（如 `deepseek-v4-pro`、`kimi-*`）不会触发本地 Anthropic 校验失败。
- 如需使用第三方模型，请在网关或 ccswitch 中做模型别名映射。

### 官方账号登录模式

- **macOS 选项 `1` / Windows 模式 `2`**
- 会修改 `app.asar`，向在线 `claude.ai` 页面注入 DOM 翻译。
- 聊天、项目、Artifacts 等远程页面会显示中文。
- Windows 下会改写 `Claude.exe` 内嵌的 asar 完整性哈希，导致 Authenticode 签名 `HashMismatch`；Cowork VM 服务可能拒绝客户端并报 `RPC pipe closed`。

---

## 卸载 / 恢复

重新运行完整安装包中的脚本：

- macOS：双击 `install-mac.command`，选择 `3`
- Windows：右键 `install-windows.bat` → 以管理员身份运行，选择 `3`

---

## 常见问题

### macOS 双击脚本提示“无法打开”

右键脚本 → 选择“打开” → 在弹出的安全提示中点击“仍要打开”。

### Windows 脚本被安全软件拦截

本脚本需要管理员权限修改 Claude Desktop 安装目录，Windows Defender 或第三方安全软件可能误报。请临时关闭实时保护，或将脚本加入白名单。

### 安装后 Claude Desktop 没有变成中文

1. 确认 Claude Desktop 已完全退出（包括菜单栏 / 托盘图标）。
2. 打开左下角账号菜单 → `Language` → 选择对应中文变体。
3. 若仍不生效，可能是 Claude 版本更新导致资源结构变化，请等待本项目更新或重新运行安装脚本。

### Cowork / 截图工作区报错

请使用 **Cowork 兼容模式**安装，并在第三方网关或 ccswitch 中做模型别名映射。

### 一键命令下载慢或失败

直接到 [Releases](https://github.com/caoergou/claude-desktop-zh-cn/releases) 页面下载 zip 或一键脚本到本地运行。

---

## 文件说明

| 文件 | 说明 |
| :--- | :--- |
| `install-mac-simple.command` | macOS 推荐版：双击自动安装 |
| `install-windows-simple.bat` | Windows 推荐版：右键管理员运行自动安装 |
| `install-mac.command` | macOS 高级版：可选择语言 / 模式 |
| `install-windows.bat` | Windows 高级版：可选择语言 / 模式 |
| `scripts/install-mac-curl.sh` | macOS 命令行一键安装脚本 |
| `scripts/install-windows-curl.bat` | Windows 命令行一键安装脚本 |
| `scripts/install-windows-curl.ps1` | Windows 一键脚本核心 |
| `scripts/patch_claude_zh_cn.py` | macOS 实际补丁逻辑 |
| `scripts/install_windows.ps1` | Windows 实际补丁逻辑 |
| `resources/frontend-zh-*.json` | 前端界面中文翻译 |
| `resources/desktop-zh-*.json` | 桌面壳层中文翻译 |
| `resources/Localizable*.strings` | macOS 原生菜单中文资源 |
| `resources/statsig-zh-*.json` | statsig i18n 兜底资源 |
| `resources/manifest*.json` | 语言包信息 |

<details>
<summary>macOS 脚本详细行为</summary>

- 安装时备份 `/Applications/Claude.app` 到同目录，命名形如 `Claude.backup-before-zh-CN-20260424-120000.app`。
- 安装前先尝试恢复旧备份以清理已有汉化；无旧备份时跳过并继续。
- 恢复 / 卸载时选择同目录下最早的 `Claude.backup-before-zh-CN-*.app` 恢复为 `/Applications/Claude.app`，并删除其他备份。
- 复制 Claude.app 到临时目录并打补丁。
- 给前端语言白名单加入当前选择的中文变体。
- 对 `Contents/Resources/app.asar` 做等长补丁，关闭 3P gateway 启动阶段的 Anthropic 名称校验；安全模式会跳过。
- 合并当前 Claude 版本的 `en-US.json` 与随包中文翻译。
- 写入 `~/Library/Application Support/Claude/config.json`，设置 `locale` 为所选语言。
- 对修改后的 Claude.app 做本机 ad-hoc 重签名，并清除 `com.apple.quarantine` 隔离属性。
- 重新启动 Claude。

</details>

<details>
<summary>Windows 脚本详细行为</summary>

- 查找 Windows 版 Claude Desktop 安装目录。
- 安装前从 `resources\.zh-cn-backups` 恢复旧备份以清理已有汉化。
- 备份被改动的前端 JS bundle、`app.asar` 和 `Claude.exe`。
- 写入随包中文资源到 `ion-dist\i18n\`、`resources\`、`ion-dist\i18n\statsig\`。
- 给前端语言白名单加入当前选择的中文变体。
- 汉化前端 bundle 中未走 i18n JSON 的硬编码界面文本。
- 官方账号登录模式会注入在线 `claude.ai` 页面 DOM 翻译。
- 写入 Windows 用户配置，将语言设置为所选语言代码。
- 重启 Claude Desktop。

</details>

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=javaht/claude-desktop-zh-cn&type=Date)](https://www.star-history.com/#javaht/claude-desktop-zh-cn&Date)

---

## 免责声明

本项目为非官方中文补丁，仅修改本机 Claude Desktop 的本地资源文件。Claude Desktop 更新后资源结构可能变化，若补丁失败，请先更新本项目或重新运行安装脚本。

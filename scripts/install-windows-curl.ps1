# 一键下载完整安装包并运行安装向导（Windows）
# 适合希望自主选择语言和模式的用户。
#
# 用法：
#   irm https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-windows-curl.ps1 | iex
#
# 环境变量（可选，用于自动化）：
#   $env:CLAUDE_ZH_VERSION       指定版本，默认 latest
#   $env:CLAUDE_ZH_LANGUAGE      zh-CN | zh-TW | zh-HK
#   $env:CLAUDE_ZH_PATCH_MODE    safe | official
#
# 示例（自动化：繁体中文 + 官方账号登录模式）：
#   $env:CLAUDE_ZH_LANGUAGE='zh-TW'; $env:CLAUDE_ZH_PATCH_MODE='official'; irm ... | iex

$ErrorActionPreference = 'Stop'

$repo = 'javaht/claude-desktop-zh-cn'
$version = if ($env:CLAUDE_ZH_VERSION) { $env:CLAUDE_ZH_VERSION } else { 'latest' }

Write-Host "正在下载 Claude Desktop 中文补丁（Windows）..." -ForegroundColor Cyan

$tmp = Join-Path $env:TEMP ('ClaudeDesktopZhCn-' + [Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tmp -Force | Out-Null

try {
    $url = if ($version -eq 'latest') {
        "https://github.com/$repo/releases/latest/download/claude-desktop-zh-cn-windows.zip"
    } else {
        "https://github.com/$repo/releases/download/$version/claude-desktop-zh-cn-windows.zip"
    }

    $zip = Join-Path $tmp 'installer.zip'
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing -MaximumRedirection 5

    Expand-Archive -Path $zip -DestinationPath $tmp -Force

    $projectDir = Join-Path $tmp 'claude-desktop-zh-cn-windows'
    $bat = Join-Path $projectDir 'install-windows.bat'
    if (-not (Test-Path $bat)) {
        throw "安装包内未找到 install-windows.bat"
    }

    # 如果用户通过环境变量指定了配置，走非交互式安装；否则启动交互式向导。
    if ($env:CLAUDE_ZH_LANGUAGE -or $env:CLAUDE_ZH_PATCH_MODE) {
        $language = if ($env:CLAUDE_ZH_LANGUAGE) { $env:CLAUDE_ZH_LANGUAGE } else { 'zh-CN' }
        $patchMode = if ($env:CLAUDE_ZH_PATCH_MODE) { $env:CLAUDE_ZH_PATCH_MODE } else { 'safe' }
        $ps1 = Join-Path $projectDir 'scripts\install_windows.ps1'
        Write-Host "正在安装：语言=$language, 模式=$patchMode ..." -ForegroundColor Cyan
        & $ps1 -Action install -Language $language -PatchMode $patchMode -Interactive:$false
    } else {
        Write-Host "正在启动安装向导，请按提示选择语言和模式..." -ForegroundColor Cyan
        Start-Process -FilePath $bat -Wait
    }
} catch {
    Write-Host "下载或运行失败：$_" -ForegroundColor Red
    Write-Host "请检查网络或版本号是否正确。" -ForegroundColor Red
    exit 1
} finally {
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}

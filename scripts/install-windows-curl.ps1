# 一键下载并运行 Claude Desktop 中文补丁（Windows）
# 用法：
#   irm https://raw.githubusercontent.com/javaht/claude-desktop-zh-cn/main/scripts/install-windows-curl.ps1 | iex
#   $env:CLAUDE_ZH_VERSION='1.3.8'; irm ... | iex   # 安装指定版本

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

    $bat = Join-Path $tmp 'claude-desktop-zh-cn-windows' 'install-windows.bat'
    if (-not (Test-Path $bat)) {
        throw "安装包内未找到 install-windows.bat"
    }

    Start-Process -FilePath $bat -Wait
} catch {
    Write-Host "下载或运行失败：$_" -ForegroundColor Red
    Write-Host "请检查网络或版本号是否正确。" -ForegroundColor Red
    exit 1
} finally {
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}

# 一键下载完整安装包并运行安装向导（Windows）
# 适合希望自主选择语言和模式的用户。

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

    Write-Host "正在启动安装向导，请按提示选择语言和模式..." -ForegroundColor Cyan
    Start-Process -FilePath $bat -Wait
} catch {
    Write-Host "下载或运行失败：$_" -ForegroundColor Red
    Write-Host "请检查网络或版本号是否正确。" -ForegroundColor Red
    exit 1
} finally {
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}

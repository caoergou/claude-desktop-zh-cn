@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1

echo ==========================================
echo   Claude Desktop 中文补丁 - Windows 简易版
echo ==========================================
echo.
echo 本脚本会自动安装：简体中文 + Cowork 兼容模式
echo 脚本会尝试自动退出 Claude Desktop；如失败请手动关闭后再运行。
echo.

set "REPO=javaht/claude-desktop-zh-cn"
set "URL=https://github.com/%REPO%/releases/latest/download/claude-desktop-zh-cn-windows.zip"
set "OUT_DIR=%TEMP%\ClaudeDesktopZhCnSimple"

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { if (Test-Path -LiteralPath '%OUT_DIR%') { Remove-Item -LiteralPath '%OUT_DIR%' -Recurse -Force }; New-Item -ItemType Directory -Path '%OUT_DIR%' -Force | Out-Null; Write-Host '正在下载安装包...' -ForegroundColor Cyan; Invoke-WebRequest -Uri '%URL%' -OutFile (Join-Path '%OUT_DIR%' 'installer.zip') -UseBasicParsing -MaximumRedirection 5; Write-Host '正在解压...' -ForegroundColor Cyan; Expand-Archive -Path (Join-Path '%OUT_DIR%' 'installer.zip') -DestinationPath '%OUT_DIR%' -Force; } catch { Write-Host ('下载失败: ' + $_.Exception.Message) -ForegroundColor Red; pause; exit 1 }"

if errorlevel 1 exit /b 1

cd /d "%OUT_DIR%\claude-desktop-zh-cn-windows"

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\install_windows.ps1" -Action install -Language zh-CN -PatchMode safe -Interactive:$false

echo.
echo 安装完成，按任意键退出。
pause >nul
exit /b 0

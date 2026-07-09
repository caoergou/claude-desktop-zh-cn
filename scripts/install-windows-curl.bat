@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1

echo ==========================================
echo   Claude Desktop 中文补丁 - Windows 下载器
echo ==========================================
echo.
echo 本脚本会下载完整安装包并启动安装向导。
echo 安装向导中可选择语言（简/繁中）和安装模式。
echo.
pause

set "REPO=javaht/claude-desktop-zh-cn"
set "ZIP_URL=https://github.com/%REPO%/releases/latest/download/claude-desktop-zh-cn-windows.zip"
set "OUT_DIR=%TEMP%\ClaudeDesktopZhCnInstaller"

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { if (Test-Path -LiteralPath '%OUT_DIR%') { Remove-Item -LiteralPath '%OUT_DIR%' -Recurse -Force }; New-Item -ItemType Directory -Path '%OUT_DIR%' -Force | Out-Null; Write-Host '正在下载安装包...' -ForegroundColor Cyan; Invoke-WebRequest -Uri '%ZIP_URL%' -OutFile (Join-Path '%OUT_DIR%' 'installer.zip') -UseBasicParsing -MaximumRedirection 5; Write-Host '正在解压...' -ForegroundColor Cyan; Expand-Archive -Path (Join-Path '%OUT_DIR%' 'installer.zip') -DestinationPath '%OUT_DIR%' -Force; $bat = Join-Path '%OUT_DIR%' 'claude-desktop-zh-cn-windows' 'install-windows.bat'; if (-not (Test-Path $bat)) { throw '安装包内未找到 install-windows.bat' }; Start-Process -FilePath $bat -Wait } catch { Write-Host ('安装失败: ' + $_.Exception.Message) -ForegroundColor Red; pause; exit 1 }"

exit /b 0

@echo off
setlocal
if "%~1"=="" (
  echo Usage: Start-OpenHands-C.cmd "C:\path\to\isolated-variant-c-repository"
  exit /b 1
)
set "PROJECT_PATH=%~f1"
if not exist "%PROJECT_PATH%\.git" (
  echo Expected an existing isolated Git repository. Nothing was changed.
  exit /b 1
)
set "DOCKER_CLI=docker"
where docker >nul 2>&1
if errorlevel 1 set "DOCKER_CLI=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe"
"%DOCKER_CLI%" version
if errorlevel 1 exit /b 1
"%DOCKER_CLI%" container inspect openhands-c-setup >nul 2>&1
if not errorlevel 1 (
  echo Container openhands-c-setup already exists. No changes were made.
  echo To start a stopped instance, use: docker start openhands-c-setup
  exit /b 1
)
"%DOCKER_CLI%" run -d --name openhands-c-setup --restart unless-stopped -p 127.0.0.1:8000:8000 -e AGENT_CANVAS_ALLOW_LAN_SESSION_KEY=true --mount "type=volume,source=openhands-c-state,target=/home/openhands/.openhands" --mount "type=bind,source=%PROJECT_PATH%,target=/projects/variant-c" ghcr.io/openhands/agent-canvas@sha256:bcdbb3fb9610f14eda67f39fc609f162ad8c3c28697d6ff3f4adae55c15c3f1d
if errorlevel 1 exit /b 1
echo Open http://localhost:8000/canvas
echo Configure the model and profile before using the single-agent API launcher.
exit /b 0

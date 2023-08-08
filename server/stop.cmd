@echo off
@REM taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.expression.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.others.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.keyboard.main:app --host 0.0.0.0 --port 8002"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.vision.main:app --host 0.0.0.0 --port 8003"

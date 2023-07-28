@echo off

@REM taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.expression.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.body.main:app --host 0.0.0.0 --port 8002"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.kernel.main:app --host 0.0.0.0 --port 8003"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.keyboard.main:app --host 0.0.0.0 --port 8004"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.ultrasound.main:app --host 0.0.0.0 --port 8005"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.vision.main:app --host 0.0.0.0 --port 8006"

@REM start cmd /k uvicorn inputs.expression.main:app --host 0.0.0.0 --port 8001
start cmd /k uvicorn inputs.body.main:app --host 0.0.0.0 --port 8002
start cmd /k uvicorn inputs.kernel.main:app --host 0.0.0.0 --port 8003
start cmd /k uvicorn inputs.keyboard.main:app --host 0.0.0.0 --port 8004
start cmd /k uvicorn inputs.ultrasound.main:app --host 0.0.0.0 --port 8005
start cmd /k uvicorn inputs.vision.main:app --host 0.0.0.0 --port 8006
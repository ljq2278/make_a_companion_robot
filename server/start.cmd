@echo off

@REM taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.expression.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.others.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.keyboard.main:app --host 0.0.0.0 --port 8002"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.vision.main:app --host 0.0.0.0 --port 8003"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  inputs.auditory.main:app --host 0.0.0.0 --port 8004"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  show_dialog:app --host 0.0.0.0 --port 8008"

@REM start cmd /k uvicorn inputs.expression.main:app --host 0.0.0.0 --port 8001
start cmd /k uvicorn inputs.others.main:app --host 0.0.0.0 --port 8001
start cmd /k uvicorn inputs.keyboard.main:app --host 0.0.0.0 --port 8002
start cmd /k uvicorn inputs.vision.main:app --host 0.0.0.0 --port 8003
start cmd /k uvicorn inputs.auditory.main:app --host 0.0.0.0 --port 8004
start cmd /k uvicorn show_dialog:app --host 0.0.0.0 --port 8008
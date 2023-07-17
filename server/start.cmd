@echo off

taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  expression.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  vision.main:app --host 0.0.0.0 --port 8002"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  auditory.main:app --host 0.0.0.0 --port 8003"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  keyboard.main:app --host 0.0.0.0 --port 8004"

start cmd /k uvicorn expression.main:app --host 0.0.0.0 --port 8001
start cmd /k uvicorn vision.main:app --host 0.0.0.0 --port 8002
start cmd /k uvicorn auditory.main:app --host 0.0.0.0 --port 8003
start cmd /k uvicorn keyboard.main:app --host 0.0.0.0 --port 8004
@echo off
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  expression.main:app --host 0.0.0.0 --port 8001"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  vision.main:app --host 0.0.0.0 --port 8002"
taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  auditory.main:app --host 0.0.0.0 --port 8003"
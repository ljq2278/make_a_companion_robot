@echo off

taskkill /FI "WINDOWTITLE eq C:\Windows\system32\cmd.exe - uvicorn  action.main:app --host 0.0.0.0 --port 8007"

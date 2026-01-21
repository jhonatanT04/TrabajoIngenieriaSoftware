@echo off
cd /d "C:\Users\mlata\Desktop\TrabajoIngenieriaSoftware\backend"
call .venv\Scripts\activate.bat
uvicorn app.main:app --reload --port 8000

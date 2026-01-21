@echo off
echo ========================================
echo INICIANDO SISTEMA MINIMERCADO
echo ========================================
echo.

REM Verificar si backend esta corriendo
echo [1/3] Verificando backend...
curl http://localhost:8000/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend NO esta corriendo
    echo.
    echo Iniciando backend...
    start "Backend" cmd /k "cd backend && .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"
    echo ✅ Backend iniciado en http://localhost:8000
    timeout /t 5 >nul
) else (
    echo ✅ Backend ya esta corriendo
)

echo.
echo [2/3] Verificando base de datos...
cd backend
.\.venv\Scripts\python -c "from app.db.database import engine; from sqlmodel import select, Session; from app.models.models import User; session = Session(engine); users = session.exec(select(User)).all(); print(f'✅ {len(users)} usuarios en DB')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Inicializando base de datos...
    .\.venv\Scripts\python reset_database.py
)
cd ..

echo.
echo [3/3] Iniciando frontend...
cd Frontend
if not exist node_modules (
    echo ⚠️  Instalando dependencias...
    call npm install
)
start "Frontend" cmd /k "ng serve --port 4200"
cd ..

echo.
echo ========================================
echo ✅ SISTEMA INICIADO
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:4200
echo Docs:     http://localhost:8000/docs
echo.
echo Usuario: admin
echo Password: admin123
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul

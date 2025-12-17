# Backend - Minimercado (FastAPI)

Este backend implementa una API REST básica para el Sistema de Gestión de Minimercado.

Características incluidas:
- Autenticación con JWT (registro y token)
- CRUD básico de productos
- Ajustes de inventario (movimientos)
- Registro de ventas simples (disminuye stock)
- CORS habilitado para desarrollo

Instalación y ejecución (Linux):

1. Crear ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configurar variables de entorno (si usa PostgreSQL):

```bash
export DATABASE_URL="postgresql+psycopg2://minimercado:1234@localhost:5432/minimercado_db"
export SECRET_KEY="cambia_esto_por_una_clave_segura"
```

Si no define DATABASE_URL, el backend usará por defecto la URL anterior (usuario `minimercado`, contraseña `1234`, BD `minimercado_db`). Asegúrese de que la base y el usuario existan (ejemplo SQL proporcionado por usted):

```sql
CREATE USER minimercado WITH PASSWORD '1234';
CREATE DATABASE minimercado_db OWNER minimercado;
```

3. Ejecutar el servidor (se crearán las tablas en la BD al iniciar si la conexión es correcta):

```bash
uvicorn backend.main:app --reload --port 8000
```

Opcional: puede crear las tablas manualmente antes de iniciar con:

```bash
python scripts/create_tables.py
```

Docs automáticas disponibles en: `http://localhost:8000/docs`

NOTA: Actualmente usa SQLite (archivo `dev.db`) para desarrollo. Para producción, cambie `DATABASE_URL` en `app/database.py` a una base Postgres y configure `SECRET_KEY` en `app/auth.py` desde variables de entorno.

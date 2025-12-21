from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Importaciones locales
from db.database import init_db, seed_data
import schemas
import deps
from endpoints import router as endpoints_router


app = FastAPI(
    title="Minimercado - Backend",
    description="API para la gestión de inventario, ventas y usuarios",
    version="1.0.0",
)

# ==================== CONFIGURACIÓN DE CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En producción usa dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== EVENTOS DE INICIO ====================
@app.on_event("startup")
def on_startup() -> None:
    """Inicializa la base de datos al arrancar el servidor"""
    init_db()
    seed_data()

# ==================== RUTAS DE SALUD / ROOT ====================
@app.get("/salud", tags=["Salud"])
def health_check():
    return {
        "status": "ok",
        "message": "Backend Minimercado funcionando correctamente",
    }

@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Bienvenido al API del Minimercado. Visita /docs para la documentación."
    }

# ==================== REGISTRAR ROUTERS ====================

# Endpoints principales
app.include_router(endpoints_router)

# Router de autenticación (opcional)
try:
    from routers.auth import router as auth_router
    app.include_router(auth_router)
except ImportError:
    pass

# ==================== USUARIO ACTUAL ====================
@app.get(
    "/users/me",
    response_model=schemas.UserRead,
    tags=["Usuarios"],
)
def read_current_user(
    current_user: schemas.UserRead = Depends(deps.get_current_user),
):
    """Devuelve la información del usuario autenticado"""
    return current_user

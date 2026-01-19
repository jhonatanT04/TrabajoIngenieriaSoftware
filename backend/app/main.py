from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db, seed_data
from app.routers import (
    router_auth,
    router_user,
    router_productos,
    router_categoria,
    router_marca,
    router_proveedor,
    router_cliente,
    router_venta,
    router_caja,
    router_inventario
)

app = FastAPI(
    title="Minimercado - Backend",
    description="API para la gestión de inventario, ventas y usuarios",
    version="1.0.0",
)

# ==================== CONFIGURACIÓN DE CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Bienvenido al API del Minimercado. Visita /docs para la documentación."
    }

# ==================== REGISTRAR ROUTERS ====================

# Endpoints principales
app.include_router(router_proveedor.router)
app.include_router(router_cliente.router)
app.include_router(router_user.router)
app.include_router(router_auth.router)
app.include_router(router_productos.router)
app.include_router(router_categoria.router)
app.include_router(router_marca.router)
app.include_router(router_venta.router)
app.include_router(router_caja.router)
app.include_router(router_inventario.router)



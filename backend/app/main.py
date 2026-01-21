from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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
    router_inventario,
    router_dashboard,
    router_reportes
)

app = FastAPI(
    title="Minimercado - Backend",
    description="API para la gestión de inventario, ventas y usuarios",
    version="1.0.0",
)

# ==================== CONFIGURACIÓN DE CORS ====================
# IMPORTANTE: Debe ser la PRIMERA configuración, ANTES de todo lo demás
# Permite que el frontend en localhost acceda a este API en cualquier puerto (dev)
allowed_origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
    max_age=3600,
)

# ==================== MANEJADORES DE EXCEPCIONES ====================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Captura errores de validación de parámetros y devuelve detalles
    """
    print("\n" + "="*60)
    print("VALIDATION ERROR DETECTED")
    print("="*60)
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Errors: {exc.errors()}")
    print(f"Body: {exc.body}")
    print("="*60 + "\n")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "url": str(request.url)
        }
    )

# ==================== EVENTOS DE INICIO ====================
# Deshabilitado temporalmente por problemas de cierre
# @app.on_event("startup")
# def on_startup() -> None:
#     """Inicializa la base de datos al arrancar el servidor"""
#     try:
#         init_db()
#         seed_data()
#     except Exception as e:
#         print(f"⚠️ Advertencia en startup: {e}")
#         # No hacer crash, solo advertir


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
app.include_router(router_dashboard.router)
app.include_router(router_reportes.router)



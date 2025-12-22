from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from deps import *
from models.models import *
from auth.auth import RoleChecker
from deps import DBSession
router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    cost_price: float
    sale_price: float
    stock_min: float = 0
    stock_max: float = 0
    is_active: bool = True

@router.post("/products", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_product(
    product_data: ProductCreate,
    db: DBSession
):
    """
    Crear un nuevo producto en el catalogo
    
    Campos requeridos:
    - name: Nombre del producto
    - sku: Codigo SKU unico
    - cost_price: Precio de costo
    - sale_price: Precio de venta
    
    Campos opcionales:
    - barcode: Codigo de barras
    - description: Descripcion del producto
    - category_id: UUID de la categoria
    - brand_id: UUID de la marca
    - stock_min: Stock minimo (default: 0)
    - stock_max: Stock maximo (default: 0)
    
    Ejemplo de Body JSON:
    ```json
    {
        "name": "Laptop HP",
        "sku": "LAP-HP-001",
        "barcode": "7891234567890",
        "cost_price": 500.00,
        "sale_price": 750.00,
        "stock_min": 5,
        "stock_max": 50
    }
    ```
    """
    from crud.products_crud import product
    
    # Verificar si el SKU ya existe
    existing = product.get_by_sku(db, sku=product_data.sku)
    if existing:
        raise HTTPException(status_code=400, detail="SKU ya existe")
    
    new_product = Product(**product_data.dict())
    created = product.create(db, obj_in=new_product)
    
    return {
        "message": "Producto creado exitosamente",
        "product": created
    }


@router.get("/products", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def list_products(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    active_only: bool = Query(True, description="Solo productos activos")
):
    """
    Listar todos los productos del catalogo
    
    Parametros de query:
    - skip: Paginacion (default: 0)
    - limit: Cantidad maxima (default: 100, max: 1000)
    - active_only: Solo activos (default: true)
    
    Retorna lista de productos con toda su informacion
    """
    from crud.products_crud import product
    
    if active_only:
        products = product.get_active_products(db)
        return products[skip:skip+limit]
    else:
        return product.get_multi(db, skip=skip, limit=limit)


@router.get("/products/{product_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador,Cajero"]))])
async def get_product(
    product_id: UUID,
    db: DBSession
):
    """
    Obtener producto especifico por ID
    
    Path params:
    - product_id: UUID del producto
    
    Retorna producto completo o 404
    """
    from crud.products_crud import product
    
    prod = product.get(db, id=product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.get("/products/sku/{sku}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador,Cajero"]))])
async def get_product_by_sku(
    sku: str,
    db: DBSession
):
    """
    Buscar producto por codigo SKU
    
    Path params:
    - sku: Codigo SKU del producto
    
    Retorna producto o 404
    """
    from crud.products_crud import product
    
    prod = product.get_by_sku(db, sku=sku)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.get("/products/barcode/{barcode}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador,Cajero"]))])
async def get_product_by_barcode(
    barcode: str,
    db: DBSession
):
    """
    Buscar producto por codigo de barras
    
    Path params:
    - barcode: Codigo de barras del producto
    
    Util para escaneo de productos
    Retorna producto o 404
    """
    from crud.products_crud import product
    
    prod = product.get_by_barcode(db, barcode=barcode)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.get("/products/search/name", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador,Cajero"]))])
async def search_products_by_name(
    db: DBSession,
    name: str = Query(..., min_length=1, description="Termino de busqueda")
):
    """
    Buscar productos por nombre (busqueda parcial)
    
    Query params:
    - name: Termino de busqueda (minimo 1 caracter)
    
    Busca coincidencias parciales en el nombre
    Retorna lista de productos que coinciden
    """
    from crud.products_crud import product
    
    products = product.search_by_name(db, name=name)
    return products


@router.get("/products/category/{category_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador,Cajero"]))])
async def get_products_by_category(
    category_id: UUID,
    db: DBSession
):
    """
    Obtener todos los productos de una categoria
    
    Path params:
    - category_id: UUID de la categoria
    
    Retorna lista de productos de esa categoria
    """
    from crud.products_crud import product
    
    products = product.get_by_category(db, category_id=category_id)
    return products


@router.get("/products/supplier/{supplier_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador,Cajero"]))])
async def get_products_by_supplier(
    supplier_id: UUID,
    db: DBSession
):
    """
    Obtener productos de un proveedor especifico
    
    Path params:
    - supplier_id: UUID del proveedor
    
    Retorna lista de productos del proveedor
    """
    from crud.products_crud import product
    
    products = product.get_by_supplier(db, supplier_id=supplier_id)
    return products


@router.get("/products/low-stock/list", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_low_stock_products(
    db: DBSession
):
    """
    Obtener productos con stock bajo
    
    Retorna productos donde el stock actual es menor al stock minimo
    Util para alertas de reabastecimiento
    """
    from crud.products_crud import product
    
    products = product.get_low_stock(db)
    return products


@router.put("/products/{product_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_product(
    product_id: UUID,
    product_data: ProductCreate,
    db: DBSession
):
    """
    Actualizar informacion de un producto
    
    Path params:
    - product_id: UUID del producto
    
    Body: Mismo formato que crear producto
    Retorna producto actualizado o 404
    """
    from crud.products_crud import product
    
    existing = product.get(db, id=product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    updated = product.update(db, db_obj=existing, obj_in=product_data.dict())
    return updated


@router.delete("/products/{product_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def deactivate_product(
    product_id: UUID,
    db: DBSession
):
    """
    Desactivar producto (soft delete)
    
    Path params:
    - product_id: UUID del producto
    
    No elimina el registro, solo marca como inactivo
    Retorna producto desactivado
    """
    from crud.products_crud import product
    
    deactivated = product.deactivate(db, id=product_id)
    return {"message": "Producto desactivado", "product": deactivated}


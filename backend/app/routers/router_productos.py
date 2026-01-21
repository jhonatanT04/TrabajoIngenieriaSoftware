from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.deps import *
from app.models.models import *
from app.auth.auth import RoleChecker
from app.deps import DBSession
router = APIRouter()


def format_product_response(product: Product):
    """Helper para formatear producto con estructura esperada por Angular"""
    return {
        "id": str(product.id),
        "sku": product.sku,
        "barcode": product.barcode,
        "name": product.name,
        "description": product.description,
        "category_id": str(product.category_id) if product.category_id else None,
        "category": {
            "id": str(product.category.id),
            "name": product.category.name,
            "description": product.category.description
        } if product.category else None,
        "brand_id": str(product.brand_id) if product.brand_id else None,
        "brand": {
            "id": str(product.brand.id),
            "name": product.brand.name,
            "description": product.brand.description
        } if product.brand else None,
        "main_supplier_id": str(product.main_supplier_id) if product.main_supplier_id else None,
        "supplier": {
            "id": str(product.supplier.id),
            "business_name": product.supplier.business_name,
            "tax_id": product.supplier.tax_id,
            "contact_name": product.supplier.contact_name,
            "email": product.supplier.email,
            "phone": product.supplier.phone,
            "address": product.supplier.address,
            "city": product.supplier.city,
            "country": product.supplier.country,
            "is_active": product.supplier.is_active
        } if product.supplier else None,
        "unit_of_measure": product.unit_of_measure,
        "sale_price": product.sale_price,
        "cost_price": product.cost_price,
        "tax_rate": product.tax_rate,
        "stock_min": product.stock_min,
        "stock_max": product.stock_max,
        "weight": product.weight,
        "requires_lot_control": product.requires_lot_control,
        "requires_expiration_date": product.requires_expiration_date,
        "is_active": product.is_active,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    }


class ProductCreate(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    main_supplier_id: Optional[UUID] = None
    unit_of_measure: str = "unidad"
    cost_price: float
    sale_price: float
    tax_rate: float = 0.0
    stock_min: float = 0
    stock_max: Optional[float] = None
    weight: Optional[float] = None
    requires_lot_control: bool = False
    requires_expiration_date: bool = False
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
    - main_supplier_id: UUID del proveedor principal
    - unit_of_measure: Unidad de medida (default: unidad)
    - tax_rate: Tasa de impuesto (default: 0.0)
    - stock_min: Stock minimo (default: 0)
    - stock_max: Stock maximo (optional)
    - weight: Peso del producto (optional)
    - requires_lot_control: Requiere control de lote (default: false)
    - requires_expiration_date: Requiere fecha de vencimiento (default: false)
    - is_active: Activo (default: true)
    """
    from app.crud.products_crud import product
    
    # Verificar si el SKU ya existe
    existing = product.get_by_sku(db, sku=product_data.sku)
    if existing:
        raise HTTPException(status_code=400, detail="SKU ya existe")
    
    new_product = Product(**product_data.dict())
    created = product.create(db, obj_in=new_product)
    
    return format_product_response(created)


@router.get("/products", tags=["Productos"])
async def list_products(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    active_only: bool = Query(True, description="Solo productos activos")
):
    """
    Listar todos los productos del catalogo (sin autenticación para desarrollo)
    
    Parametros de query:
    - skip: Paginacion (default: 0)
    - limit: Cantidad maxima (default: 100, max: 1000)
    - active_only: Solo activos (default: true)
    
    Retorna lista de productos con toda su informacion
    """
    from app.crud.products_crud import product
    
    if active_only:
        products = product.get_active_products(db)
        filtered = products[skip:skip+limit]
    else:
        filtered = product.get_multi(db, skip=skip, limit=limit)
    
    return [format_product_response(p) for p in filtered]


@router.get("/products/{product_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
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
    from app.crud.products_crud import product
    
    prod = product.get(db, id=product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return format_product_response(prod)


@router.get("/products/sku/{sku}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
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
    from app.crud.products_crud import product
    
    prod = product.get_by_sku(db, sku=sku)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return format_product_response(prod)


@router.get("/products/barcode/{barcode}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
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
    from app.crud.products_crud import product
    
    prod = product.get_by_barcode(db, barcode=barcode)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return format_product_response(prod)


@router.get("/products/search/name", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
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
    from app.crud.products_crud import product
    
    products = product.search_by_name(db, name=name)
    return [format_product_response(p) for p in products]


@router.get("/products/category/{category_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
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
    from app.crud.products_crud import product
    
    products = product.get_by_category(db, category_id=category_id)
    return [format_product_response(p) for p in products]


@router.get("/products/supplier/{supplier_id}", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
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
    from app.crud.products_crud import product
    
    products = product.get_by_supplier(db, supplier_id=supplier_id)
    return [format_product_response(p) for p in products]


@router.get("/products/low-stock/list", tags=["Productos"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_low_stock_products(
    db: DBSession
):
    """
    Obtener productos con stock bajo
    
    Retorna productos donde el stock actual es menor al stock minimo
    Util para alertas de reabastecimiento
    """
    from app.crud.products_crud import product
    
    products = product.get_low_stock(db)
    return [format_product_response(p) for p in products]


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
    from app.crud.products_crud import product
    
    existing = product.get(db, id=product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    updated = product.update(db, db_obj=existing, obj_in=product_data.dict())
    return format_product_response(updated)


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
    from app.crud.products_crud import product
    
    deactivated = product.deactivate(db, id=product_id)
    return format_product_response(deactivated)


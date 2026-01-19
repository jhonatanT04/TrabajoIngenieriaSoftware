from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.models.models import Supplier
from app.deps import DBSession
from app.auth.auth import RoleChecker
router = APIRouter()



class SupplierCreate(BaseModel):
    business_name: str
    tax_id: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True


@router.post("/suppliers", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_supplier(
    supplier_data: SupplierCreate,
    db: DBSession
):
    """
    Crear nuevo proveedor
    
    Campos requeridos:
    - business_name: Razon social
    - tax_id: RUC del proveedor
    
    Campos opcionales:
    - contact_name: Nombre de contacto
    - phone: Telefono
    - email: Correo
    - address: Direccion
    
    Ejemplo de Body JSON:
    ```json
    {
        "business_name": "Distribuidora XYZ",
        "tax_id": "1234567890001",
        "contact_name": "Maria Garcia",
        "phone": "0999999999",
        "email": "contacto@xyz.com"
    }
    ```
    """
    from crud.proovider_crud import supplier
    
    existing = supplier.get_by_tax_id(db, tax_id=supplier_data.tax_id)
    if existing:
        raise HTTPException(status_code=400, detail="Proveedor con este RUC ya existe")
    
    new_supplier = Supplier(**supplier_data.dict())
    created = supplier.create(db, obj_in=new_supplier)
    
    return {
        "message": "Proveedor creado exitosamente",
        "supplier": created
    }


@router.get("/suppliers", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_suppliers(
    db: DBSession,
    active_only: bool = Query(True, description="Solo proveedores activos")
):
    """
    Listar todos los proveedores
    
    Query params:
    - active_only: Solo activos (default: true)
    
    Retorna lista de proveedores
    """
    from crud.proovider_crud import supplier
    
    if active_only:
        return supplier.get_active_suppliers(db)


class InventoryUpdate(BaseModel):
    product_id: UUID
    location_id: Optional[UUID] = None
    quantity: float


@router.post("/inventory/update-stock", tags=["Inventario"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_inventory_stock(
    data: InventoryUpdate,
    db: DBSession,
    user_id: UUID = Body(...)
):
    """
    Actualizar stock de inventario
    
    Body JSON:
    {
        "product_id": "uuid-here",
        "quantity": 100.0,
        "user_id": "uuid-here"
    }
    """
    from crud.inventario_crud import inventory
    
    updated = inventory.update_stock(
        db,
        product_id=data.product_id,
        location_id=data.location_id,
        quantity=data.quantity,
        user_id=user_id
    )
    
    return {
        "message": "Stock actualizado exitosamente",
        "inventory": updated
    }


@router.get("/inventory/product/{product_id}", tags=["Inventario"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_product_inventory(
    product_id: UUID,
    db: DBSession
):
    """Obtener inventario de un producto"""
    from crud.inventario_crud import inventory
    
    inventories = inventory.get_by_product(db, product_id=product_id)
    total_stock = inventory.get_total_stock_by_product(db, product_id=product_id)
    
    return {
        "product_id": product_id,
        "total_stock": total_stock,
        "locations": inventories
    }


@router.get("/inventory/location/{location_id}", tags=["Inventario"])
async def get_location_inventory(
    location_id: UUID,
    db: DBSession
):
    """Obtener inventario por ubicación"""
    from crud.inventario_crud import inventory
    
    inventories = inventory.get_by_location(db, location_id=location_id)
    return inventories

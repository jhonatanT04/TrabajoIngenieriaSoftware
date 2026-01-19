from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.deps import DBSession
from app.models.models import Inventory, InventoryMovement, Product
from app.auth.auth import RoleChecker

router = APIRouter()

class InventoryUpdateRequest(BaseModel):
    product_id: UUID
    quantity: float
    reason: Optional[str] = None

class InventoryAdjustmentRequest(BaseModel):
    product_id: UUID
    new_quantity: float
    reason: str

@router.get("/inventory", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_inventory(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_id: Optional[UUID] = None,
    low_stock: bool = False
):
    """
    Listar inventario
    """
    query = db.query(Inventory)
    
    if product_id:
        query = query.filter(Inventory.product_id == product_id)
    
    if low_stock:
        # Obtener productos con stock bajo
        query = query.join(Product).filter(Inventory.quantity <= Product.stock_min)
    
    inventory = query.offset(skip).limit(limit).all()
    return inventory

@router.get("/inventory/{product_id}", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_product_inventory(
    product_id: UUID,
    db: DBSession
):
    """
    Obtener inventario de un producto
    """
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    return inventory

@router.post("/inventory/adjustment", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def adjust_inventory(
    adjustment_data: InventoryAdjustmentRequest,
    db: DBSession
):
    """
    Ajustar inventario de un producto
    """
    inventory = db.query(Inventory).filter(Inventory.product_id == adjustment_data.product_id).first()
    
    if not inventory:
        # Crear nuevo registro de inventario
        inventory = Inventory(
            product_id=adjustment_data.product_id,
            quantity=adjustment_data.new_quantity,
            updated_by=None  # Se debe obtener del usuario actual
        )
        db.add(inventory)
    else:
        # Registrar movimiento
        movement = InventoryMovement(
            product_id=adjustment_data.product_id,
            movement_type="ajuste",
            quantity=adjustment_data.new_quantity - inventory.quantity,
            previous_stock=inventory.quantity,
            new_stock=adjustment_data.new_quantity,
            reason=adjustment_data.reason,
            user_id=None  # Se debe obtener del usuario actual
        )
        db.add(movement)
        
        # Actualizar inventario
        inventory.quantity = adjustment_data.new_quantity
        inventory.last_updated = datetime.utcnow()
        inventory.updated_by = None  # Se debe obtener del usuario actual
    
    db.commit()
    db.refresh(inventory)
    
    return inventory

@router.get("/inventory/movements", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_inventory_movements(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_id: Optional[UUID] = None,
    movement_type: Optional[str] = None
):
    """
    Listar movimientos de inventario
    """
    query = db.query(InventoryMovement)
    
    if product_id:
        query = query.filter(InventoryMovement.product_id == product_id)
    
    if movement_type:
        query = query.filter(InventoryMovement.movement_type == movement_type)
    
    movements = query.order_by(InventoryMovement.created_at.desc()).offset(skip).limit(limit).all()
    return movements

@router.get("/inventory/movements/{product_id}", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_product_movements(
    product_id: UUID,
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500)
):
    """
    Obtener movimientos de inventario de un producto
    """
    movements = db.query(InventoryMovement).filter(
        InventoryMovement.product_id == product_id
    ).order_by(InventoryMovement.created_at.desc()).offset(skip).limit(limit).all()
    
    return movements

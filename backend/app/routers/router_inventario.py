from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import select

from app.deps import DBSession
from app.models.models import Inventory, InventoryMovement, Product
from app.auth.auth import RoleChecker, get_current_user

router = APIRouter()


def format_inventory_item(item: Inventory):
    """Formatear item de inventario"""
    return {
        "id": str(item.id),
        "product_id": str(item.product_id),
        "location_id": str(item.location_id) if item.location_id else None,
        "quantity": item.quantity,
        "last_updated": item.last_updated.isoformat() if item.last_updated else None,
        "updated_by": str(item.updated_by) if item.updated_by else None
    }


def format_movement(movement: InventoryMovement):
    """Formatear movimiento de inventario"""
    return {
        "id": str(movement.id),
        "product_id": str(movement.product_id),
        "movement_type": movement.movement_type.value if hasattr(movement.movement_type, 'value') else str(movement.movement_type),
        "quantity": movement.quantity,
        "previous_stock": movement.previous_stock,
        "new_stock": movement.new_stock,
        "reason": movement.reason,
        "reference_document": movement.reference_document,
        "user_id": str(movement.user_id),
        "created_at": movement.created_at.isoformat() if hasattr(movement, 'created_at') else None
    }


class InventoryAdjustmentRequest(BaseModel):
    product_id: UUID
    new_quantity: float
    reason: str


@router.get("/inventory", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_inventory(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_id: Optional[UUID] = None,
    low_stock: bool = Query(False)
):
    """
    Listar inventario
    
    Query params:
    - skip: Paginación (default: 0)
    - limit: Límite de registros (default: 100)
    - product_id: Filtrar por producto (opcional)
    - low_stock: Si es true, retorna solo stock bajo (opcional)
    """
    query = select(Inventory)
    
    if product_id:
        query = query.where(Inventory.product_id == product_id)
    
    # Ejecutar query base
    inventory_items = db.exec(query.offset(skip).limit(limit)).all()
    
    # Filtrar por stock bajo si se pide
    if low_stock:
        filtered_items = []
        for item in inventory_items:
            if item.product and item.quantity <= item.product.stock_min:
                filtered_items.append(item)
        inventory_items = filtered_items
    
    return [format_inventory_item(i) for i in inventory_items]


@router.get("/inventory/movement-list", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_inventory_movements(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Listar movimientos de inventario con filtros opcionales
    
    Query params:
    - skip: Paginación (default: 0)
    - limit: Límite (default: 100)
    - product_id: Filtrar por producto (opcional, UUID como string)
    - start_date: Fecha inicio ISO8601 (opcional)
    - end_date: Fecha fin ISO8601 (opcional)
    """
    # Validar límites
    if skip < 0:
        skip = 0
    if limit < 1:
        limit = 1
    if limit > 1000:
        limit = 1000
    
    query = select(InventoryMovement)
    
    # Validar product_id si se proporciona
    if product_id and product_id.strip():
        try:
            product_uuid = UUID(product_id.strip())
            query = query.where(InventoryMovement.product_id == product_uuid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"product_id inválido: debe ser un UUID válido"
            )
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.where(InventoryMovement.created_at >= start)
        except:
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.where(InventoryMovement.created_at <= end)
        except:
            pass
    
    query = query.order_by(InventoryMovement.created_at.desc())
    movements = db.exec(query.offset(skip).limit(limit)).all()
    
    return [format_movement(m) for m in movements]


@router.get("/inventory/{product_id}", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_product_inventory(
    product_id: UUID,
    db: DBSession
):
    """
    Obtener inventario de un producto específico
    
    Path params:
    - product_id: UUID del producto
    """
    query = select(Inventory).where(Inventory.product_id == product_id)
    inventory = db.exec(query).first()
    
    if not inventory:
        # Si no existe inventario, retornar uno vacío en lugar de 404
        # Verificar que el producto existe
        from app.models.models import Product
        product = db.exec(select(Product).where(Product.id == product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Retornar inventario con cantidad 0
        return {
            "id": None,
            "product_id": str(product_id),
            "location_id": None,
            "quantity": 0,
            "last_updated": None,
            "updated_by": None
        }
    
    return format_inventory_item(inventory)


@router.post("/inventory/adjustment", tags=["Inventario"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def adjust_inventory(
    adjustment_data: InventoryAdjustmentRequest,
    db: DBSession,
    current_user = Depends(get_current_user)
):
    """
    Ajustar inventario de un producto
    
    Body JSON:
    {
        "product_id": "uuid",
        "new_quantity": 100,
        "reason": "Ajuste de inventario"
    }
    """
    # Obtener inventario existente
    query = select(Inventory).where(Inventory.product_id == adjustment_data.product_id)
    inventory = db.exec(query).first()
    
    previous_stock = inventory.quantity if inventory else 0
    
    if not inventory:
        # Crear nuevo registro
        inventory = Inventory(
            product_id=adjustment_data.product_id,
            quantity=adjustment_data.new_quantity,
            last_updated=datetime.utcnow(),
            updated_by=current_user.id
        )
        db.add(inventory)
    else:
        # Actualizar inventario existente
        inventory.quantity = adjustment_data.new_quantity
        inventory.last_updated = datetime.utcnow()
        inventory.updated_by = current_user.id
    
    # SIEMPRE registrar movimiento (nuevo o actualización)
    movement = InventoryMovement(
        product_id=adjustment_data.product_id,
        movement_type="ajuste",
        quantity=adjustment_data.new_quantity - previous_stock,
        previous_stock=previous_stock,
        new_stock=adjustment_data.new_quantity,
        reason=adjustment_data.reason,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(movement)
    
    db.commit()
    db.refresh(inventory)
    
    return format_inventory_item(inventory)


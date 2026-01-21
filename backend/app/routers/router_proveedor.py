from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.models.models import Supplier, PurchaseOrder, PurchaseOrderDetail, Product
from app.deps import DBSession
from app.auth.auth import RoleChecker, get_current_user
from app.models.enums import OrderStatus
router = APIRouter()


def format_supplier_response(supplier: Supplier):
    """Helper para formatear proveedor con estructura esperada por Angular"""
    return {
        "id": str(supplier.id),
        "business_name": supplier.business_name,
        "tax_id": supplier.tax_id,
        "contact_name": supplier.representative_name,
        "email": supplier.email,
        "phone": supplier.phone,
        "address": supplier.address,
        "city": None,  # Campos opcionales no presentes
        "country": None,
        "is_active": supplier.is_active,
        "created_at": supplier.created_at.isoformat(),
        "updated_at": supplier.updated_at.isoformat()
    }


def format_purchase_order_response(order: PurchaseOrder):
    """Helper para formatear orden de compra"""
    return {
        "id": str(order.id),
        "order_number": order.order_number,
        "supplier_id": str(order.supplier_id),
        "order_date": order.order_date.isoformat(),
        "expected_delivery_date": order.expected_delivery_date.isoformat() if order.expected_delivery_date else None,
        "actual_delivery_date": order.actual_delivery_date.isoformat() if hasattr(order, 'actual_delivery_date') and order.actual_delivery_date else None,
        "status": order.status.value if hasattr(order.status, 'value') else str(order.status),
        "items": [
            {
                "id": str(detail.id),
                "product_id": str(detail.product_id),
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
                "subtotal": detail.subtotal
            }
            for detail in order.details
        ] if order.details else [],
        "total_amount": sum(detail.subtotal for detail in order.details) if order.details else 0.0,
        "notes": getattr(order, 'notes', None)
    }


class SupplierCreate(BaseModel):
    business_name: str
    tax_id: str
    contact_name: Optional[str] = None  # Mapped to representative_name
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_days: Optional[int] = None
    is_active: bool = True


class SupplierUpdate(BaseModel):
    business_name: Optional[str] = None
    tax_id: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_days: Optional[int] = None
    is_active: Optional[bool] = None


class PurchaseOrderItemCreate(BaseModel):
    product_id: UUID
    quantity: float
    unit_price: float


class PurchaseOrderCreate(BaseModel):
    supplier_id: UUID
    expected_delivery_date: Optional[datetime] = None
    items: list[PurchaseOrderItemCreate]
    notes: Optional[str] = None


# ==================== ENDPOINTS DE PROVEEDORES ====================

@router.post("/suppliers", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_supplier(
    supplier_data: SupplierCreate,
    db: DBSession
):
    """
    Crear nuevo proveedor
    
    Campos requeridos:
    - business_name: Razón social
    - tax_id: RUC/NIT del proveedor
    
    Campos opcionales:
    - contact_name: Nombre de contacto
    - phone: Teléfono
    - email: Correo
    - address: Dirección
    """
    from app.crud.proovider_crud import supplier
    
    existing = supplier.get_by_tax_id(db, tax_id=supplier_data.tax_id)
    if existing:
        raise HTTPException(status_code=400, detail="Proveedor con este RUC ya existe")
    
    # Convertir contact_name a representative_name
    data_dict = supplier_data.dict()
    if 'contact_name' in data_dict:
        data_dict['representative_name'] = data_dict.pop('contact_name')
    
    new_supplier = Supplier(**data_dict)
    created = supplier.create(db, obj_in=new_supplier)
    
    return format_supplier_response(created)


@router.get("/suppliers", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def list_suppliers(
    db: DBSession,
    q: Optional[str] = Query(None, description="Búsqueda por nombre o RUC"),
    active_only: bool = Query(True, description="Solo proveedores activos")
):
    """
    Listar todos los proveedores
    
    Query params:
    - q: Búsqueda por nombre o RUC (opcional)
    - active_only: Solo activos (default: true)
    """
    from app.crud.proovider_crud import supplier
    
    if active_only:
        suppliers = supplier.get_active_suppliers(db)
    else:
        suppliers = supplier.get_multi(db)
    
    # Filtrar por búsqueda si se proporciona
    if q:
        suppliers = [
            s for s in suppliers
            if q.lower() in s.business_name.lower() or q.lower() in s.tax_id.lower()
        ]
    
    return [format_supplier_response(s) for s in suppliers]


@router.get("/suppliers/{supplier_id}", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_supplier(
    supplier_id: UUID,
    db: DBSession
):
    """
    Obtener un proveedor por ID
    """
    from app.crud.proovider_crud import supplier
    
    supplier_obj = supplier.get(db, id=supplier_id)
    if not supplier_obj:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return format_supplier_response(supplier_obj)


@router.put("/suppliers/{supplier_id}", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_supplier(
    supplier_id: UUID,
    supplier_data: SupplierUpdate,
    db: DBSession
):
    """
    Actualizar un proveedor existente
    """
    from app.crud.proovider_crud import supplier
    
    existing = supplier.get(db, id=supplier_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Convertir contact_name a representative_name
    data_dict = supplier_data.dict(exclude_unset=True)
    if 'contact_name' in data_dict:
        data_dict['representative_name'] = data_dict.pop('contact_name')
    
    updated = supplier.update(db, db_obj=existing, obj_in=data_dict)
    return format_supplier_response(updated)


@router.delete("/suppliers/{supplier_id}", tags=["Proveedores"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def delete_supplier(
    supplier_id: UUID,
    db: DBSession
):
    """
    Desactivar un proveedor (soft delete)
    """
    from app.crud.proovider_crud import supplier
    
    existing = supplier.get(db, id=supplier_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    existing.is_active = False
    existing.updated_at = datetime.utcnow()
    db.add(existing)
    db.commit()
    db.refresh(existing)
    
    return format_supplier_response(existing)


# ==================== ENDPOINTS DE ÓRDENES DE COMPRA ====================

@router.post("/ordenes-compra", tags=["Órdenes de Compra"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_purchase_order(
    order_data: PurchaseOrderCreate,
    db: DBSession,
    current_user = Depends(get_current_user)
):
    """
    Crear nueva orden de compra
    
    Body JSON:
    {
        "supplier_id": "uuid",
        "expected_delivery_date": "2025-02-20T00:00:00",
        "items": [
            {
                "product_id": "uuid",
                "quantity": 100,
                "unit_price": 50.00
            }
        ],
        "notes": "Nota opcional"
    }
    """
    from app.crud.proovider_crud import purchase_order, purchase_order_detail
    
    # Generar número de orden
    last_order = db.exec(
        __import__('sqlmodel').select(PurchaseOrder)
        .order_by(PurchaseOrder.order_date.desc())
        .limit(1)
    ).first()
    order_number = f"PO-{datetime.utcnow().strftime('%Y%m%d')}-{len([last_order]) + 1:04d}"
    
    # Crear orden
    new_order = PurchaseOrder(
        order_number=order_number,
        supplier_id=order_data.supplier_id,
        expected_delivery_date=order_data.expected_delivery_date,
        created_by_user_id=current_user.id,
        status=OrderStatus.pendiente
    )
    
    db.add(new_order)
    db.flush()  # Obtener ID
    
    # Agregar items
    for item in order_data.items:
        detail = PurchaseOrderDetail(
            purchase_order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price
        )
        db.add(detail)
    
    db.commit()
    db.refresh(new_order)
    
    return format_purchase_order_response(new_order)


@router.get("/ordenes-compra", tags=["Órdenes de Compra"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_purchase_orders(
    db: DBSession,
    supplier_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(100)
):
    """
    Listar órdenes de compra
    
    Query params:
    - supplier_id: Filtrar por proveedor (opcional)
    - status: Filtrar por estado (optional)
    - skip/limit: Paginación
    """
    from sqlmodel import select
    
    query = select(PurchaseOrder)
    
    if supplier_id:
        query = query.where(PurchaseOrder.supplier_id == supplier_id)
    
    if status:
        query = query.where(PurchaseOrder.status == status)
    
    orders = db.exec(query.offset(skip).limit(limit)).all()
    return [format_purchase_order_response(o) for o in orders]


@router.get("/ordenes-compra/{order_id}", tags=["Órdenes de Compra"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_purchase_order(
    order_id: UUID,
    db: DBSession
):
    """
    Obtener una orden de compra por ID
    """
    from sqlmodel import select
    
    order = db.exec(select(PurchaseOrder).where(PurchaseOrder.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    return format_purchase_order_response(order)


@router.put("/ordenes-compra/{order_id}", tags=["Órdenes de Compra"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_purchase_order(
    order_id: UUID,
    order_data: PurchaseOrderCreate,
    db: DBSession
):
    """
    Actualizar una orden de compra
    """
    from sqlmodel import select
    
    order = db.exec(select(PurchaseOrder).where(PurchaseOrder.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    # Solo permitir actualizar si está pendiente
    if order.status != OrderStatus.pendiente:
        raise HTTPException(status_code=400, detail="Solo se pueden actualizar órdenes pendientes")
    
    order.supplier_id = order_data.supplier_id
    order.expected_delivery_date = order_data.expected_delivery_date
    
    # Actualizar items
    for detail in order.details:
        db.delete(detail)
    
    for item in order_data.items:
        detail = PurchaseOrderDetail(
            purchase_order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price
        )
        db.add(detail)
    
    db.commit()
    db.refresh(order)
    
    return format_purchase_order_response(order)


@router.post("/ordenes-compra/{order_id}/cancelar", tags=["Órdenes de Compra"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def cancel_purchase_order(
    order_id: UUID,
    data: dict = Body(...),
    db: DBSession = None
):
    """
    Cancelar una orden de compra
    
    Body JSON:
    {
        "motivo": "Razón de cancelación"
    }
    """
    from sqlmodel import select
    
    order = db.exec(select(PurchaseOrder).where(PurchaseOrder.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    order.status = OrderStatus.cancelada
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return format_purchase_order_response(order)


@router.post("/ordenes-compra/{order_id}/aprobar", tags=["Órdenes de Compra"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def approve_purchase_order(
    order_id: UUID,
    db: DBSession
):
    """
    Aprobar una orden de compra
    """
    from sqlmodel import select
    
    order = db.exec(select(PurchaseOrder).where(PurchaseOrder.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    if order.status != OrderStatus.pendiente:
        raise HTTPException(status_code=400, detail="La orden debe estar pendiente para aprobar")
    
    order.status = OrderStatus.recibida
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return format_purchase_order_response(order)

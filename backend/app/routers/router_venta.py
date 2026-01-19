from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.deps import DBSession
from app.models.models import Sale, SaleDetail, Customer
from app.auth.auth import RoleChecker

router = APIRouter()

class SaleItemCreate(BaseModel):
    product_id: UUID
    quantity: float
    unit_price: float
    discount: float = 0.0

class SaleCreate(BaseModel):
    customer_id: Optional[UUID] = None
    cash_register_id: UUID
    items: List[SaleItemCreate]
    payment_method_id: UUID
    payment_amount: float
    notes: Optional[str] = None

@router.post("/sales", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def create_sale(
    sale_data: SaleCreate,
    db: DBSession
):
    """
    Crear una nueva venta
    """
    # Calcular totales
    subtotal = sum(item.quantity * item.unit_price for item in sale_data.items)
    discount_total = sum(item.discount for item in sale_data.items)
    tax = subtotal * 0.12  # IVA 12%
    total = subtotal - discount_total + tax
    
    # Crear venta
    sale = Sale(
        customer_id=sale_data.customer_id,
        cash_register_id=sale_data.cash_register_id,
        cashier_id=None,  # Se debe obtener del usuario actual
        subtotal=subtotal,
        discount=discount_total,
        tax=tax,
        total=total,
        status="completada"
    )
    
    db.add(sale)
    db.commit()
    db.refresh(sale)
    
    # Crear detalles de venta
    for item in sale_data.items:
        detail = SaleDetail(
            sale_id=sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=item.discount,
            subtotal=item.quantity * item.unit_price - item.discount
        )
        db.add(detail)
    
    db.commit()
    db.refresh(sale)
    
    return sale

@router.get("/sales", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_sales(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Listar ventas con filtros opcionales
    """
    query = db.query(Sale)
    
    if customer_id:
        query = query.filter(Sale.customer_id == customer_id)
    if start_date:
        query = query.filter(Sale.created_at >= start_date)
    if end_date:
        query = query.filter(Sale.created_at <= end_date)
    
    sales = query.offset(skip).limit(limit).all()
    return sales

@router.get("/sales/{sale_id}", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_sale(
    sale_id: UUID,
    db: DBSession
):
    """
    Obtener detalles de una venta
    """
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return sale

@router.delete("/sales/{sale_id}", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def delete_sale(
    sale_id: UUID,
    db: DBSession
):
    """
    Anular una venta
    """
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    sale.status = "anulada"
    db.commit()
    
    return {"message": "Venta anulada correctamente"}

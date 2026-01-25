from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import select

from app.deps import DBSession
from app.models.models import Sale, SaleDetail, Customer, CashRegister, PaymentMethod, Inventory, InventoryMovement, Product, CashTransaction, CashRegisterSession, User
from app.auth.auth import RoleChecker, get_current_user
from app.models.enums import SaleStatus, MovementType, TransactionType, SessionStatus

router = APIRouter()


def format_sale_response(sale: Sale, product_map: dict | None = None):
    """Formatear venta con estructura esperada por Angular"""
    return {
        "id": str(sale.id),
        "sale_number": sale.sale_number,
        "sale_date": sale.sale_date.isoformat(),
        "cashier_id": str(sale.cashier_id),
        "cash_register_id": str(sale.cash_register_id),
        "customer_id": str(sale.customer_id) if sale.customer_id else None,
        "customer": {
            "id": str(sale.customer.id),
            "document_number": sale.customer.document_number,
            "first_name": sale.customer.first_name,
            "last_name": sale.customer.last_name
        } if sale.customer else None,
        "cashier": {
            "id": str(sale.cashier.id),
            "username": sale.cashier.username,
            "first_name": sale.cashier.first_name,
            "last_name": sale.cashier.last_name
        } if sale.cashier else None,
        "subtotal": sale.subtotal,
        "discount_amount": sale.discount_amount,
        "tax_amount": sale.tax_amount,
        "total_amount": sale.total_amount,
        "status": sale.status.value if hasattr(sale.status, 'value') else str(sale.status),
        "items": [
            {
                "id": str(detail.id),
                "product_id": str(detail.product_id),
                "product_name": (
                    detail.product.name
                    if getattr(detail, "product", None) and getattr(detail.product, "name", None)
                    else product_map.get(detail.product_id) if product_map else None
                ),
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
                "discount_percentage": detail.discount_percentage,
                "discount_amount": detail.discount_amount,
                "subtotal": detail.subtotal,
                "tax_rate": detail.tax_rate,
                "tax_amount": detail.tax_amount,
                "total": detail.total
            }
            for detail in sale.details
        ] if sale.details else [],
        "notes": sale.notes,
        "created_at": sale.created_at.isoformat()
    }


class SaleItemCreate(BaseModel):
    product_id: UUID
    quantity: float
    unit_price: float
    discount_percentage: float = 0.0
    tax_rate: float = 0.0


class SaleCreate(BaseModel):
    customer_id: Optional[UUID] = None
    cash_register_id: Optional[UUID] = None
    payment_method_id: Optional[UUID] = None
    items: List[SaleItemCreate]
    notes: Optional[str] = None


@router.post("/sales", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def create_sale(
    sale_data: SaleCreate,
    db: DBSession,
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva venta
    
    Body JSON:
    {
        "customer_id": "uuid (optional)",
        "cash_register_id": "uuid",
        "payment_method_id": "uuid",
        "items": [
            {
                "product_id": "uuid",
                "quantity": 2,
                "unit_price": 100.00,
                "discount_percentage": 0,
                "tax_rate": 0.19
            }
        ],
        "notes": "Notas de la venta (optional)"
    }
    """
    from app.crud.sale_crud import sale as sale_crud
    
    # Validar que el usuario tenga una sesión de caja abierta
    active_session = db.exec(
        select(CashRegisterSession).where(
            CashRegisterSession.user_id == current_user.id,
            CashRegisterSession.status == SessionStatus.abierta
        )
    ).first()
    if not active_session:
        raise HTTPException(
            status_code=400,
            detail="Debes abrir una caja antes de registrar ventas"
        )

    # Generar número de venta único
    import datetime as dt
    from sqlmodel import func
    
    today_start = dt.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = dt.datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
    
    count_query = select(func.count(Sale.id)).where(
        Sale.sale_date >= today_start,
        Sale.sale_date <= today_end
    )
    today_count = db.exec(count_query).first() or 0
    sale_number = f"V-{dt.datetime.utcnow().strftime('%Y%m%d')}-{today_count + 1:05d}"
    
    # Resolver caja y método de pago: forzamos la caja de la sesión activa del cajero
    sale_data.cash_register_id = active_session.cash_register_id
    if not sale_data.payment_method_id:
        payment_method = db.exec(select(PaymentMethod)).first()
        if not payment_method:
            raise HTTPException(status_code=400, detail="No hay métodos de pago configurados")
        sale_data.payment_method_id = payment_method.id
    
    # Calcular totales
    subtotal = 0.0
    discount_total = 0.0
    tax_total = 0.0
    
    # ⭐ VALIDAR STOCK DISPONIBLE PARA CADA PRODUCTO
    for item in sale_data.items:
        inventory_query = select(Inventory).where(Inventory.product_id == item.product_id)
        inventory = db.exec(inventory_query).first()
        
        if not inventory or inventory.quantity < item.quantity:
            available = inventory.quantity if inventory else 0
            product_query = select(Product).where(Product.id == item.product_id)
            product = db.exec(product_query).first()
            product_name = product.name if product else "Producto desconocido"
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para {product_name}. Solicitado: {item.quantity}, Disponible: {available}"
            )
    
    for item in sale_data.items:
        item_subtotal = item.quantity * item.unit_price
        item_discount = item_subtotal * (item.discount_percentage / 100)
        item_tax = (item_subtotal - item_discount) * item.tax_rate
        
        subtotal += item_subtotal
        discount_total += item_discount
        tax_total += item_tax
    
    total = subtotal - discount_total + tax_total
    
    # Crear venta
    new_sale = Sale(
        sale_number=sale_number,
        sale_date=dt.datetime.utcnow(),
        cashier_id=current_user.id,
        cash_register_id=sale_data.cash_register_id,
        customer_id=sale_data.customer_id,
        subtotal=subtotal,
        discount_amount=discount_total,
        tax_amount=tax_total,
        total_amount=total,
        status=SaleStatus.completada,
        notes=sale_data.notes,
        created_at=dt.datetime.utcnow()
    )
    
    db.add(new_sale)
    db.flush()  # Obtener ID
    
    # Crear detalles
    for item in sale_data.items:
        item_subtotal = item.quantity * item.unit_price
        item_discount = item_subtotal * (item.discount_percentage / 100)
        item_tax = (item_subtotal - item_discount) * item.tax_rate
        item_total = item_subtotal - item_discount + item_tax
        
        detail = SaleDetail(
            sale_id=new_sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_percentage=item.discount_percentage,
            discount_amount=item_discount,
            subtotal=item_subtotal,
            tax_rate=item.tax_rate,
            tax_amount=item_tax,
            total=item_total
        )
        db.add(detail)
        
        # ⭐ DESCONTAR DEL INVENTARIO
        inventory_query = select(Inventory).where(Inventory.product_id == item.product_id)
        inventory = db.exec(inventory_query).first()
        
        if inventory:
            inventory.quantity -= item.quantity
            db.add(inventory)
        
        # ⭐ CREAR MOVIMIENTO DE INVENTARIO (SALIDA POR VENTA)
        previous_stock = inventory.quantity if inventory else 0  # Stock antes de la salida
        new_stock = previous_stock - item.quantity  # Stock después de la salida
        
        movement = InventoryMovement(
            product_id=item.product_id,
            movement_type=MovementType.salida,
            quantity=item.quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            unit_cost=item.unit_price,
            total_cost=item.quantity * item.unit_price,
            reference_document=f"Venta {sale_number}",
            user_id=current_user.id,
            movement_date=dt.datetime.utcnow(),
            created_at=dt.datetime.utcnow()
        )
        db.add(movement)
    
    # ⭐ CREAR TRANSACCIÓN DE CAJA PARA LA VENTA
    # Buscar sesión de caja abierta para esta caja registradora
    active_session_query = select(CashRegisterSession).where(
        CashRegisterSession.cash_register_id == sale_data.cash_register_id,
        CashRegisterSession.status == SessionStatus.abierta
    )
    active_session = db.exec(active_session_query).first()
    
    if active_session:
        # Crear transacción de tipo venta
        cash_transaction = CashTransaction(
            session_id=active_session.id,
            transaction_type=TransactionType.venta,
            amount=total,
            payment_method_id=sale_data.payment_method_id,
            reference_number=sale_number,
            description=f"Venta {sale_number}",
            created_by=current_user.id,
            created_at=dt.datetime.utcnow()
        )
        db.add(cash_transaction)
    
    db.commit()
    db.refresh(new_sale)
    
    return format_sale_response(new_sale)


@router.get("/sales", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_sales(
    db: DBSession,
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None
):
    """
    Listar ventas.
    Admin ve todas las ventas, Cajero solo ve las de su caja activa.
    
    Query params:
    - skip: Paginación (default: 0)
    - limit: Límite (default: 100)
    - customer_id: Filtrar por cliente (optional)
    - status: Filtrar por estado (optional)
    """
    from app.crud.users_crud import profile
    
    query = select(Sale)
    
    # Verificar si es admin o cajero
    user_profile = profile.get(db, id=current_user.profile_id)
    is_admin = user_profile and user_profile.name.upper() in ["ADMIN", "ADMINISTRADOR"]
    
    # Si es cajero, filtrar por su caja activa
    if not is_admin:
        # Obtener sesión activa del cajero
        active_session = db.exec(
            select(CashRegisterSession).where(
                CashRegisterSession.user_id == current_user.id,
                CashRegisterSession.status == SessionStatus.abierta
            )
        ).first()
        
        if active_session:
            query = query.where(Sale.cash_register_id == active_session.cash_register_id)
        else:
            # Si no tiene sesión activa, filtrar por cashier_id para que al menos vea sus propias ventas
            query = query.where(Sale.cashier_id == current_user.id)
    
    if customer_id:
        query = query.where(Sale.customer_id == customer_id)
    
    if status:
        query = query.where(Sale.status == status)
    
    sales = db.exec(query.offset(skip).limit(limit)).all()

    # Prefetch product names for all sale details to avoid missing product_name
    product_ids = set()
    for s in sales:
        if s.details:
            for d in s.details:
                if d.product_id:
                    product_ids.add(d.product_id)

    product_map = {}
    if product_ids:
        products = db.exec(select(Product).where(Product.id.in_(product_ids))).all()
        product_map = {p.id: p.name for p in products}
    
    return [format_sale_response(s, product_map) for s in sales]


@router.get("/sales/{sale_id}", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_sale(
    sale_id: UUID,
    db: DBSession
):
    """
    Obtener una venta específica por ID
    """
    query = select(Sale).where(Sale.id == sale_id)
    sale = db.exec(query).first()
    
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    return format_sale_response(sale)


@router.delete("/sales/{sale_id}", tags=["Ventas"])
async def delete_sale(
    sale_id: UUID,
    db: DBSession
):
    """
    Eliminar una venta (sin autenticación para desarrollo)
    ⭐ NOTA: El stock NO se restaura. Se mantiene deducido después de eliminar la venta.
    Solo se elimina el registro de la transacción.
    """
    query = select(Sale).where(Sale.id == sale_id)
    sale = db.exec(query).first()
    
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    # Obtener movimientos de inventario de esta venta para eliminarlos
    # (NO restauramos el stock, solo eliminamos el registro del movimiento)
    status_value = sale.status.value if hasattr(sale.status, 'value') else str(sale.status)
    if status_value == 'completada':
        movement_query = select(InventoryMovement).where(
            InventoryMovement.reference_document.like(f"%Venta {sale.sale_number}%")
        )
        movements = db.exec(movement_query).all()
        
        # Eliminar movimientos de inventario (SIN restaurar stock)
        for movement in movements:
            db.delete(movement)
    
    # Eliminar detalles de venta
    for detail in sale.details:
        db.delete(detail)
    
    # Eliminar venta
    db.delete(sale)
    db.commit()
    
    return {"message": "Venta eliminada correctamente. Stock permanece deducido.", "id": str(sale_id)}


@router.post("/sales/{sale_id}/cancelar", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def cancel_sale(
    sale_id: UUID,
    data: dict = Body(...),
    db: DBSession = None
):
    """
    Cancelar una venta
    
    Body JSON:
    {
        "motivo": "Razón de cancelación"
    }
    """
    query = select(Sale).where(Sale.id == sale_id)
    sale = db.exec(query).first()
    
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    if sale.status == SaleStatus.cancelada:
        raise HTTPException(status_code=400, detail="La venta ya está cancelada")
    
    sale.status = SaleStatus.cancelada
    db.add(sale)
    db.commit()
    db.refresh(sale)
    
    return format_sale_response(sale)


@router.get("/sales/por-fecha", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_sales_by_date(
    db: DBSession,
    fechaInicio: str = Query(...),
    fechaFin: str = Query(...)
):
    """
    Obtener ventas por rango de fecha
    
    Query params:
    - fechaInicio: Fecha inicio ISO8601 (required)
    - fechaFin: Fecha fin ISO8601 (required)
    """
    try:
        start = datetime.fromisoformat(fechaInicio)
        end = datetime.fromisoformat(fechaFin)
    except:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido")
    
    query = select(Sale).where(
        Sale.sale_date >= start,
        Sale.sale_date <= end
    )
    
    sales = db.exec(query).all()
    
    return [format_sale_response(s) for s in sales]


@router.get("/sales/cliente/{customer_id}", tags=["Ventas"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_sales_by_customer(
    customer_id: UUID,
    db: DBSession,
    skip: int = Query(0),
    limit: int = Query(100)
):
    """
    Obtener ventas de un cliente específico
    """
    query = select(Sale).where(Sale.customer_id == customer_id)
    
    sales = db.exec(query.offset(skip).limit(limit)).all()
    
    return [format_sale_response(s) for s in sales]

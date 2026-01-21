from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import select, or_

from app.deps import DBSession, get_current_user
from app.models.models import Customer, User
from app.auth.auth import RoleChecker

router = APIRouter()

# ========== SCHEMAS ==========
class CustomerCreate(BaseModel):
    document_number: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    is_active: bool = True
    
    class Config:
        extra = 'ignore'

class CustomerUpdate(BaseModel):
    document_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = None

# ========== HELPER FUNCTIONS ==========
def format_customer_response(customer: Customer) -> dict:
    """
    Formatea un cliente según lo esperado por el frontend Angular
    """
    return {
        "id": str(customer.id),
        "document_number": customer.document_number,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "city": customer.city,
        "loyalty_points": customer.loyalty_points,
        "is_active": customer.is_active,
        "created_at": customer.created_at.isoformat(),
        "updated_at": customer.updated_at.isoformat()
    }

# ========== ENDPOINTS ==========
@router.post("/customers", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def create_customer(
    customer_data: CustomerCreate,
    db: DBSession,
    current_user: User = Depends(get_current_user)
):
    """
    Crear nuevo cliente
    """
    # Verificar si ya existe cliente con ese documento
    if customer_data.document_number:
        existing_query = select(Customer).where(Customer.document_number == customer_data.document_number)
        existing = db.exec(existing_query).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cliente con este documento ya existe"
            )
    
    # Crear nuevo cliente
    new_customer = Customer(
        document_number=customer_data.document_number,
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        email=customer_data.email,
        phone=customer_data.phone,
        address=customer_data.address,
        city=customer_data.city,
        is_active=customer_data.is_active,
        loyalty_points=0.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return format_customer_response(new_customer)

@router.get("/customers", tags=["Clientes"])
async def list_customers(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    active_only: bool = Query(True, description="Solo clientes activos")
):
    """
    Listar todos los clientes con paginación (sin autenticación para desarrollo)
    """
    query = select(Customer)
    
    if active_only:
        query = query.where(Customer.is_active == True)
    
    # Ordenar por fecha de creación descendente
    query = query.order_by(Customer.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    customers = db.exec(query).all()
    return [format_customer_response(customer) for customer in customers]

@router.get("/customers/{customer_id}", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_customer(
    customer_id: UUID,
    db: DBSession
):
    """
    Obtener cliente específico por ID
    """
    customer = db.exec(select(Customer).where(Customer.id == customer_id)).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return format_customer_response(customer)

@router.get("/customers/document/{document_number}", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_customer_by_document(
    document_number: str,
    db: DBSession
):
    """
    Buscar cliente por número de documento (cédula o RUC)
    """
    customer = db.exec(
        select(Customer).where(Customer.document_number == document_number)
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return format_customer_response(customer)

@router.get("/customers/search/name", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def search_customers_by_name(
    db: DBSession,
    name: str = Query(..., min_length=2, description="Término de búsqueda")
):
    """
    Buscar clientes por nombre o apellido (búsqueda parcial)
    """
    search_term = f"%{name}%"
    query = select(Customer).where(
        or_(
            Customer.first_name.ilike(search_term),
            Customer.last_name.ilike(search_term)
        )
    )
    
    customers = db.exec(query).all()
    return [format_customer_response(customer) for customer in customers]

@router.put("/customers/{customer_id}", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def update_customer(
    customer_id: UUID,
    customer_data: CustomerUpdate,
    db: DBSession
):
    """
    Actualizar datos de un cliente
    """
    customer = db.exec(select(Customer).where(Customer.id == customer_id)).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    # Actualizar campos proporcionados
    update_data = customer_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    customer.updated_at = datetime.utcnow()
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    return format_customer_response(customer)

@router.delete("/customers/{customer_id}", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def delete_customer(
    customer_id: UUID,
    db: DBSession
):
    """
    Desactivar un cliente (soft delete)
    """
    customer = db.exec(select(Customer).where(Customer.id == customer_id)).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    customer.is_active = False
    customer.updated_at = datetime.utcnow()
    
    db.add(customer)
    db.commit()
    
    return {"message": "Cliente desactivado exitosamente"}

@router.post("/customers/{customer_id}/loyalty-points", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def update_loyalty_points(
    customer_id: UUID,
    db: DBSession,
    points: float = Body(..., embed=True)
):
    """
    Actualizar puntos de fidelidad de un cliente
    
    Suma los puntos al total existente.
    Para canjear puntos, enviar valor negativo.
    
    Body JSON:
    {
        "points": 50.0
    }
    """
    customer = db.exec(select(Customer).where(Customer.id == customer_id)).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    # Sumar puntos (pueden ser positivos o negativos)
    customer.loyalty_points += points
    
    # No permitir puntos negativos
    if customer.loyalty_points < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Puntos insuficientes para canjear"
        )
    
    customer.updated_at = datetime.utcnow()
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    return format_customer_response(customer)

@router.get("/customers/vip/list", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_vip_customers(
    db: DBSession
):
    """
    Listar clientes VIP (segment = 'vip')
    """
    query = select(Customer).where(
        Customer.segment == "vip",
        Customer.is_active == True
    )
    
    customers = db.exec(query).all()
    return [format_customer_response(customer) for customer in customers]

@router.get("/customers/top/list", tags=["Clientes"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_top_customers(
    db: DBSession,
    limit: int = Query(10, ge=1, le=50, description="Cantidad de clientes top")
):
    """
    Top clientes por puntos de fidelidad
    """
    query = select(Customer).where(Customer.is_active == True)
    query = query.order_by(Customer.loyalty_points.desc())
    query = query.limit(limit)
    
    customers = db.exec(query).all()
    return [format_customer_response(customer) for customer in customers]

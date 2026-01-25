from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.deps import DBSession, get_current_user
from app.models.models import CashRegisterSession, CashRegister, CashTransaction, User, TransactionType, SessionStatus
from app.auth.auth import RoleChecker

router = APIRouter(
    prefix="/caja",
    tags=["Caja"]
)

# ========== SCHEMAS ==========
class CashRegisterResponse(BaseModel):
    id: str
    register_number: str
    location: Optional[str] = None
    is_active: bool

class SessionOpenRequest(BaseModel):
    cash_register_id: UUID
    opening_amount: float
    notes: Optional[str] = None

class SessionCloseRequest(BaseModel):
    actual_closing_amount: float
    notes: Optional[str] = None

class TransactionCreate(BaseModel):
    transaction_type: str  # ingreso, egreso, venta
    amount: float
    payment_method_id: UUID
    reference_number: Optional[str] = None
    description: Optional[str] = None

# ========== HELPER FUNCTIONS ==========
def format_cash_session(session: CashRegisterSession) -> dict:
    """
    Formatea una sesión de caja según lo esperado por el frontend Angular
    """
    # Cargar relación del usuario si no está cargada
    user_data = None
    if session.user:
        user_data = {
            "id": str(session.user.id),
            "first_name": session.user.first_name,
            "last_name": session.user.last_name,
            "email": session.user.email
        }
    
    return {
        "id": str(session.id),
        "cash_register_id": str(session.cash_register_id),
        "user_id": str(session.user_id),
        "user": user_data,
        "opening_date": session.opening_date.isoformat(),
        "closing_date": session.closing_date.isoformat() if session.closing_date else None,
        "opening_amount": session.opening_amount,
        "expected_closing_amount": session.expected_closing_amount,
        "actual_closing_amount": session.actual_closing_amount,
        "difference": session.difference,
        "status": session.status.value if hasattr(session.status, 'value') else session.status,
        "notes": session.notes
    }

def format_cash_transaction(transaction: CashTransaction) -> dict:
    """
    Formatea una transacción de caja según lo esperado por el frontend Angular
    """
    return {
        "id": str(transaction.id),
        "session_id": str(transaction.session_id),
        "transaction_type": transaction.transaction_type.value if hasattr(transaction.transaction_type, 'value') else transaction.transaction_type,
        "amount": transaction.amount,
        "payment_method_id": str(transaction.payment_method_id),
        "reference_number": transaction.reference_number,
        "description": transaction.description,
        "created_at": transaction.created_at.isoformat(),
        "created_by": str(transaction.created_by)
    }

# ========== ENDPOINTS ==========
@router.get("/cash-registers", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_cash_registers(
    db: DBSession,
    current_user: User = Depends(get_current_user),
    is_active: Optional[bool] = Query(True, description="Filtrar por cajas activas")
):
    """
    Obtener lista de cajas registradoras disponibles
    """
    query = select(CashRegister)
    if is_active is not None:
        query = query.where(CashRegister.is_active == is_active)
    
    cash_registers = db.exec(query.order_by(CashRegister.register_number)).all()
    
    return {
        "success": True,
        "data": [
            {
                "id": str(cr.id),
                "register_number": cr.register_number,
                "location": cr.location,
                "is_active": cr.is_active
            }
            for cr in cash_registers
        ]
    }

@router.post("/cash-sessions/open", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def open_cash_session(
    session_data: SessionOpenRequest,
    db: DBSession,
    current_user: User = Depends(get_current_user)
):
    """
    Abrir una sesión de caja
    """
    # Verificar que no haya sesión abierta en esta caja
    query = select(CashRegisterSession).where(
        CashRegisterSession.cash_register_id == session_data.cash_register_id,
        CashRegisterSession.status == SessionStatus.abierta
    )
    existing_session = db.exec(query).first()
    
    if existing_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una sesión abierta para esta caja"
        )
    
    # Verificar que la caja existe
    cash_register = db.exec(select(CashRegister).where(CashRegister.id == session_data.cash_register_id)).first()
    if not cash_register:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caja registradora no encontrada"
        )
    
    # Crear nueva sesión
    session = CashRegisterSession(
        cash_register_id=session_data.cash_register_id,
        user_id=current_user.id,
        opening_amount=session_data.opening_amount,
        expected_closing_amount=0.0,
        actual_closing_amount=0.0,
        difference=0.0,
        status=SessionStatus.abierta,
        notes=session_data.notes,
        opening_date=datetime.utcnow()
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return format_cash_session(session)

@router.post("/cash-sessions/{session_id}/close", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def close_cash_session(
    session_id: UUID,
    close_data: SessionCloseRequest,
    db: DBSession,
    current_user: User = Depends(get_current_user)
):
    """
    Cerrar una sesión de caja
    """
    # Obtener sesión
    session = db.exec(select(CashRegisterSession).options(selectinload(CashRegisterSession.user)).where(CashRegisterSession.id == session_id)).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    if session.status != SessionStatus.abierta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sesión ya está cerrada"
        )
    
    # Calcular el monto esperado (apertura + transacciones)
    transactions_query = select(CashTransaction).where(CashTransaction.session_id == session_id)
    transactions = db.exec(transactions_query).all()
    
    expected_amount = session.opening_amount
    for trans in transactions:
        trans_type = trans.transaction_type.value if hasattr(trans.transaction_type, 'value') else trans.transaction_type
        if trans_type in ["ingreso", "venta"]:
            expected_amount += trans.amount
        elif trans_type == "egreso":
            expected_amount -= trans.amount
    
    # Actualizar sesión
    session.closing_date = datetime.utcnow()
    session.expected_closing_amount = expected_amount
    session.actual_closing_amount = close_data.actual_closing_amount
    session.difference = close_data.actual_closing_amount - expected_amount
    session.status = SessionStatus.cerrada
    if close_data.notes:
        session.notes = close_data.notes
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return format_cash_session(session)

@router.get("/cash-sessions", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_cash_sessions(
    db: DBSession,
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """
    Listar sesiones de caja con paginación y filtros.
    Admin ve todas las sesiones, Cajero solo ve las suyas.
    """
    from app.crud.users_crud import profile
    
    query = select(CashRegisterSession).options(selectinload(CashRegisterSession.user))
    
    # Obtener perfil del usuario para determinar si es admin o cajero
    user_profile = profile.get(db, id=current_user.profile_id)
    is_admin = user_profile and user_profile.name.upper() in ["ADMIN", "ADMINISTRADOR"]
    
    # Si es cajero, filtrar solo sus sesiones
    if not is_admin:
        query = query.where(CashRegisterSession.user_id == current_user.id)
    
    if status:
        try:
            status_enum = SessionStatus(status)
            query = query.where(CashRegisterSession.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido: {status}"
            )
    
    # Ordenar por fecha de apertura descendente
    query = query.order_by(CashRegisterSession.opening_date.desc())
    query = query.offset(skip).limit(limit)
    
    sessions = db.exec(query).all()
    return [format_cash_session(session) for session in sessions]

@router.get("/cash-sessions/{session_id}", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_cash_session(
    session_id: UUID,
    db: DBSession
):
    """
    Obtener detalles de una sesión de caja específica
    """
    session = db.exec(select(CashRegisterSession).options(selectinload(CashRegisterSession.user)).where(CashRegisterSession.id == session_id)).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    return format_cash_session(session)

@router.post("/cash-sessions/{session_id}/transactions", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def create_cash_transaction(
    session_id: UUID,
    transaction_data: TransactionCreate,
    db: DBSession,
    current_user: User = Depends(get_current_user)
):
    """
    Registrar una transacción de caja (ingreso/egreso)
    """
    # Verificar que la sesión existe y está abierta
    session = db.exec(select(CashRegisterSession).where(CashRegisterSession.id == session_id)).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    if session.status != SessionStatus.abierta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sesión no está abierta"
        )
    
    # Validar tipo de transacción
    try:
        trans_type = TransactionType(transaction_data.transaction_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de transacción inválido: {transaction_data.transaction_type}"
        )
    
    # Crear transacción
    transaction = CashTransaction(
        session_id=session_id,
        transaction_type=trans_type,
        amount=transaction_data.amount,
        payment_method_id=transaction_data.payment_method_id,
        reference_number=transaction_data.reference_number,
        description=transaction_data.description,
        created_at=datetime.utcnow(),
        created_by=current_user.id
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return format_cash_transaction(transaction)

@router.get("/cash-sessions/{session_id}/transactions", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_session_transactions(
    session_id: UUID,
    db: DBSession
):
    """
    Listar todas las transacciones de una sesión de caja
    """
    # Verificar que la sesión existe
    session = db.exec(select(CashRegisterSession).where(CashRegisterSession.id == session_id)).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    # Obtener transacciones
    query = select(CashTransaction).where(CashTransaction.session_id == session_id)
    query = query.order_by(CashTransaction.created_at.desc())
    transactions = db.exec(query).all()
    
    return [format_cash_transaction(trans) for trans in transactions]

@router.get("/cash-sessions/user/active", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_active_session(
    db: DBSession,
    current_user: User = Depends(get_current_user)
):
    """
    Obtener la sesión de caja abierta actualmente para el usuario autenticado
    """
    query = select(CashRegisterSession).options(selectinload(CashRegisterSession.user)).where(
        CashRegisterSession.user_id == current_user.id,
        CashRegisterSession.status == SessionStatus.abierta
    )
    session = db.exec(query).first()
    
    if not session:
        return None
    
    # Incluir información del usuario
    result = format_cash_session(session)
    result["user"] = {
        "id": str(current_user.id),
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }
    
    return result

@router.get("/cash-sessions/status/summary", dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_cash_sessions_summary(
    db: DBSession
):
    """
    Obtener resumen de todas las sesiones de caja abiertas (solo admin)
    """
    query = select(CashRegisterSession).options(selectinload(CashRegisterSession.user)).where(
        CashRegisterSession.status == SessionStatus.abierta
    )
    query = query.order_by(CashRegisterSession.opening_date.desc())
    sessions = db.exec(query).all()
    
    result = {
        "total_open_sessions": len(sessions),
        "sessions": [],
        "total_in_registers": 0.0
    }
    
    for session in sessions:
        session_data = format_cash_session(session)
        session_data["user"] = {
            "id": str(session.user.id),
            "username": session.user.username,
            "first_name": session.user.first_name,
            "last_name": session.user.last_name
        }
        result["sessions"].append(session_data)
        result["total_in_registers"] += session.opening_amount
    
    return result

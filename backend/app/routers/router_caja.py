from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import select

from app.deps import DBSession, get_current_user
from app.models.models import CashRegisterSession, CashRegister, CashTransaction, User, TransactionType, SessionStatus
from app.auth.auth import RoleChecker

router = APIRouter()

# ========== SCHEMAS ==========
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
    return {
        "id": str(session.id),
        "cash_register_id": str(session.cash_register_id),
        "user_id": str(session.user_id),
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
@router.post("/cash-sessions/open", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
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

@router.post("/cash-sessions/{session_id}/close", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
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
    session = db.exec(select(CashRegisterSession).where(CashRegisterSession.id == session_id)).first()
    
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

@router.get("/cash-sessions", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_cash_sessions(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """
    Listar sesiones de caja con paginación y filtros
    """
    query = select(CashRegisterSession)
    
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

@router.get("/cash-sessions/{session_id}", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_cash_session(
    session_id: UUID,
    db: DBSession
):
    """
    Obtener detalles de una sesión de caja específica
    """
    session = db.exec(select(CashRegisterSession).where(CashRegisterSession.id == session_id)).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    return format_cash_session(session)

@router.post("/cash-sessions/{session_id}/transactions", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
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

@router.get("/cash-sessions/{session_id}/transactions", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
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

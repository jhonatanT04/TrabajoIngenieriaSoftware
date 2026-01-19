from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.deps import DBSession
from app.models.models import CashRegisterSession, CashRegister, CashTransaction, TransactionType
from app.auth.auth import RoleChecker

router = APIRouter()

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

@router.post("/cash-sessions/open", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def open_cash_session(
    session_data: SessionOpenRequest,
    db: DBSession
):
    """
    Abrir una sesión de caja
    """
    # Verificar que no haya sesión abierta
    existing_session = db.query(CashRegisterSession).filter(
        CashRegisterSession.cash_register_id == session_data.cash_register_id,
        CashRegisterSession.status == "abierta"
    ).first()
    
    if existing_session:
        raise HTTPException(status_code=400, detail="Ya existe una sesión abierta para esta caja")
    
    session = CashRegisterSession(
        cash_register_id=session_data.cash_register_id,
        user_id=None,  # Se debe obtener del usuario actual
        opening_amount=session_data.opening_amount,
        status="abierta",
        notes=session_data.notes
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session

@router.post("/cash-sessions/{session_id}/close", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def close_cash_session(
    session_id: UUID,
    close_data: SessionCloseRequest,
    db: DBSession
):
    """
    Cerrar una sesión de caja
    """
    session = db.query(CashRegisterSession).filter(CashRegisterSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    if session.status != "abierta":
        raise HTTPException(status_code=400, detail="La sesión ya está cerrada")
    
    # Calcular el monto esperado (apertura + transacciones)
    total_transactions = db.query(CashTransaction).filter(
        CashTransaction.session_id == session_id
    ).all()
    
    expected_amount = session.opening_amount
    for trans in total_transactions:
        if trans.transaction_type == "ingreso" or trans.transaction_type == "venta":
            expected_amount += trans.amount
        else:
            expected_amount -= trans.amount
    
    session.closing_date = datetime.utcnow()
    session.expected_closing_amount = expected_amount
    session.actual_closing_amount = close_data.actual_closing_amount
    session.difference = close_data.actual_closing_amount - expected_amount
    session.status = "cerrada"
    session.notes = close_data.notes
    
    db.commit()
    db.refresh(session)
    
    return session

@router.get("/cash-sessions", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_cash_sessions(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """
    Listar sesiones de caja
    """
    query = db.query(CashRegisterSession)
    
    if status:
        query = query.filter(CashRegisterSession.status == status)
    
    sessions = query.offset(skip).limit(limit).all()
    return sessions

@router.get("/cash-sessions/{session_id}", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def get_cash_session(
    session_id: UUID,
    db: DBSession
):
    """
    Obtener detalles de una sesión de caja
    """
    session = db.query(CashRegisterSession).filter(CashRegisterSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return session

@router.post("/cash-sessions/{session_id}/transactions", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def create_cash_transaction(
    session_id: UUID,
    transaction_data: TransactionCreate,
    db: DBSession
):
    """
    Registrar una transacción de caja
    """
    session = db.query(CashRegisterSession).filter(CashRegisterSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    if session.status != "abierta":
        raise HTTPException(status_code=400, detail="La sesión no está abierta")
    
    transaction = CashTransaction(
        session_id=session_id,
        transaction_type=transaction_data.transaction_type,
        amount=transaction_data.amount,
        payment_method_id=transaction_data.payment_method_id,
        reference_number=transaction_data.reference_number,
        description=transaction_data.description,
        created_by=None  # Se debe obtener del usuario actual
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction

@router.get("/cash-sessions/{session_id}/transactions", tags=["Caja"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador", "Cajero"]))])
async def list_session_transactions(
    session_id: UUID,
    db: DBSession
):
    """
    Listar transacciones de una sesión de caja
    """
    transactions = db.query(CashTransaction).filter(
        CashTransaction.session_id == session_id
    ).all()
    
    return transactions

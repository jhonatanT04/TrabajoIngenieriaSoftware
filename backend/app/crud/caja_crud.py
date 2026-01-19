"""
CRUD para módulos de Caja y Clientes
Archivo: backend/app/crud/crud_cash_customers.py
"""
from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from app.models.models import (
    CashRegister, CashRegisterSession, PaymentMethod, CashTransaction,
    SalePayment, CashCount, CashCountDetail, Customer, CustomerPreference,
    LoyaltyTransaction, CustomerNotification, SessionStatus, TransactionType,
    LoyaltyTransactionType
)
from .base_crud import CRUDBase


# ==================== CAJA ====================
class CRUDCashRegister(CRUDBase[CashRegister, CashRegister, CashRegister]):
    def get_by_register_number(
        self, 
        db: Session, 
        *, 
        register_number: str
    ) -> Optional[CashRegister]:
        """Obtener caja por número"""
        statement = select(CashRegister).where(
            CashRegister.register_number == register_number
        )
        return db.exec(statement).first()
    
    def get_active_registers(self, db: Session) -> List[CashRegister]:
        """Obtener cajas activas"""
        statement = select(CashRegister).where(CashRegister.is_active == True)
        return db.exec(statement).all()


class CRUDCashRegisterSession(CRUDBase[CashRegisterSession, CashRegisterSession, CashRegisterSession]):
    def get_by_cash_register(
        self, 
        db: Session, 
        *, 
        cash_register_id: UUID
    ) -> List[CashRegisterSession]:
        """Obtener sesiones de una caja"""
        statement = select(CashRegisterSession).where(
            CashRegisterSession.cash_register_id == cash_register_id
        ).order_by(CashRegisterSession.opening_date.desc())
        return db.exec(statement).all()
    
    def get_by_user(self, db: Session, *, user_id: UUID) -> List[CashRegisterSession]:
        """Obtener sesiones de un usuario"""
        statement = select(CashRegisterSession).where(
            CashRegisterSession.user_id == user_id
        )
        return db.exec(statement).all()
    
    def get_open_sessions(self, db: Session) -> List[CashRegisterSession]:
        """Obtener sesiones abiertas"""
        statement = select(CashRegisterSession).where(
            CashRegisterSession.status == SessionStatus.abierta
        )
        return db.exec(statement).all()
    
    def get_current_session(
        self, 
        db: Session, 
        *, 
        cash_register_id: UUID,
        user_id: UUID
    ) -> Optional[CashRegisterSession]:
        """Obtener sesión actual abierta de un usuario en una caja"""
        statement = select(CashRegisterSession).where(
            CashRegisterSession.cash_register_id == cash_register_id,
            CashRegisterSession.user_id == user_id,
            CashRegisterSession.status == SessionStatus.abierta
        )
        return db.exec(statement).first()
    
    def close_session(
        self, 
        db: Session, 
        *, 
        id: UUID,
        actual_closing_amount: float
    ) -> CashRegisterSession:
        """Cerrar sesión de caja"""
        session = self.get(db, id)
        session.closing_date = datetime.utcnow()
        session.actual_closing_amount = actual_closing_amount
        session.difference = actual_closing_amount - session.expected_closing_amount
        session.status = SessionStatus.cerrada
        db.add(session)
        db.commit()
        db.refresh(session)
        return session


class CRUDPaymentMethod(CRUDBase[PaymentMethod, PaymentMethod, PaymentMethod]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[PaymentMethod]:
        """Obtener método de pago por nombre"""
        statement = select(PaymentMethod).where(PaymentMethod.name == name)
        return db.exec(statement).first()
    
    def get_active_methods(self, db: Session) -> List[PaymentMethod]:
        """Obtener métodos de pago activos"""
        statement = select(PaymentMethod).where(PaymentMethod.is_active == True)
        return db.exec(statement).all()


class CRUDCashTransaction(CRUDBase[CashTransaction, CashTransaction, CashTransaction]):
    def get_by_session(self, db: Session, *, session_id: UUID) -> List[CashTransaction]:
        """Obtener transacciones de una sesión"""
        statement = select(CashTransaction).where(
            CashTransaction.session_id == session_id
        ).order_by(CashTransaction.created_at.desc())
        return db.exec(statement).all()
    
    def get_by_type(
        self, 
        db: Session, 
        *, 
        transaction_type: TransactionType
    ) -> List[CashTransaction]:
        """Obtener transacciones por tipo"""
        statement = select(CashTransaction).where(
            CashTransaction.transaction_type == transaction_type
        )
        return db.exec(statement).all()


class CRUDSalePayment(CRUDBase[SalePayment, SalePayment, SalePayment]):
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> List[SalePayment]:
        """Obtener pagos de una venta"""
        statement = select(SalePayment).where(SalePayment.sale_id == sale_id)
        return db.exec(statement).all()
    
    def get_by_payment_method(
        self, 
        db: Session, 
        *, 
        payment_method_id: UUID
    ) -> List[SalePayment]:
        """Obtener pagos por método"""
        statement = select(SalePayment).where(
            SalePayment.payment_method_id == payment_method_id
        )
        return db.exec(statement).all()


class CRUDCashCount(CRUDBase[CashCount, CashCount, CashCount]):
    def get_by_session(self, db: Session, *, session_id: UUID) -> List[CashCount]:
        """Obtener arqueos de una sesión"""
        statement = select(CashCount).where(
            CashCount.session_id == session_id
        ).order_by(CashCount.count_date.desc())
        return db.exec(statement).all()
    
    def get_with_details(self, db: Session, *, id: UUID) -> Optional[CashCount]:
        """Obtener arqueo con sus detalles"""
        cash_count = self.get(db, id)
        if cash_count:
            _ = cash_count.details
        return cash_count


class CRUDCashCountDetail(CRUDBase[CashCountDetail, CashCountDetail, CashCountDetail]):
    def get_by_cash_count(self, db: Session, *, cash_count_id: UUID) -> List[CashCountDetail]:
        """Obtener detalles de un arqueo"""
        statement = select(CashCountDetail).where(
            CashCountDetail.cash_count_id == cash_count_id
        )
        return db.exec(statement).all()


# ==================== CLIENTES ====================
class CRUDCustomer(CRUDBase[Customer, Customer, Customer]):
    def get_by_document(self, db: Session, *, document_number: str) -> Optional[Customer]:
        """Obtener cliente por documento"""
        statement = select(Customer).where(Customer.document_number == document_number)
        return db.exec(statement).first()
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[Customer]:
        """Obtener cliente por email"""
        statement = select(Customer).where(Customer.email == email)
        return db.exec(statement).first()
    
    def search_by_name(self, db: Session, *, name: str) -> List[Customer]:
        """Buscar clientes por nombre"""
        statement = select(Customer).where(
            Customer.first_name.contains(name) | Customer.last_name.contains(name)
        )
        return db.exec(statement).all()
    
    def get_active_customers(self, db: Session) -> List[Customer]:
        """Obtener clientes activos"""
        statement = select(Customer).where(Customer.is_active == True)
        return db.exec(statement).all()
    
    def get_by_segment(self, db: Session, *, segment: str) -> List[Customer]:
        """Obtener clientes por segmento"""
        statement = select(Customer).where(Customer.segment == segment)
        return db.exec(statement).all()
    
    def get_vip_customers(self, db: Session) -> List[Customer]:
        """Obtener clientes VIP"""
        return self.get_by_segment(db, segment="VIP")
    
    def update_loyalty_points(
        self, 
        db: Session, 
        *, 
        id: UUID, 
        points: float
    ) -> Customer:
        """Actualizar puntos de fidelidad"""
        customer = self.get(db, id)
        customer.loyalty_points += points
        customer.updated_at = datetime.utcnow()
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    
    def get_top_customers(
        self, 
        db: Session, 
        *, 
        limit: int = 10
    ) -> List[Customer]:
        """Obtener mejores clientes por puntos de fidelidad"""
        statement = select(Customer).where(
            Customer.is_active == True
        ).order_by(Customer.loyalty_points.desc()).limit(limit)
        return db.exec(statement).all()


class CRUDCustomerPreference(CRUDBase[CustomerPreference, CustomerPreference, CustomerPreference]):
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[CustomerPreference]:
        """Obtener preferencias de un cliente"""
        statement = select(CustomerPreference).where(
            CustomerPreference.customer_id == customer_id
        ).order_by(CustomerPreference.purchase_frequency.desc())
        return db.exec(statement).all()
    
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[CustomerPreference]:
        """Obtener clientes que prefieren un producto"""
        statement = select(CustomerPreference).where(
            CustomerPreference.product_id == product_id
        )
        return db.exec(statement).all()


class CRUDLoyaltyTransaction(CRUDBase[LoyaltyTransaction, LoyaltyTransaction, LoyaltyTransaction]):
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[LoyaltyTransaction]:
        """Obtener transacciones de fidelidad de un cliente"""
        statement = select(LoyaltyTransaction).where(
            LoyaltyTransaction.customer_id == customer_id
        ).order_by(LoyaltyTransaction.created_at.desc())
        return db.exec(statement).all()
    
    def get_by_type(
        self, 
        db: Session, 
        *, 
        transaction_type: LoyaltyTransactionType
    ) -> List[LoyaltyTransaction]:
        """Obtener transacciones por tipo"""
        statement = select(LoyaltyTransaction).where(
            LoyaltyTransaction.transaction_type == transaction_type
        )
        return db.exec(statement).all()
    
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> Optional[LoyaltyTransaction]:
        """Obtener transacción de fidelidad de una venta"""
        statement = select(LoyaltyTransaction).where(
            LoyaltyTransaction.sale_id == sale_id
        )
        return db.exec(statement).first()


class CRUDCustomerNotification(CRUDBase[CustomerNotification, CustomerNotification, CustomerNotification]):
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[CustomerNotification]:
        """Obtener notificaciones de un cliente"""
        statement = select(CustomerNotification).where(
            CustomerNotification.customer_id == customer_id
        ).order_by(CustomerNotification.sent_date.desc())
        return db.exec(statement).all()
    
    def get_pending_notifications(self, db: Session) -> List[CustomerNotification]:
        """Obtener notificaciones pendientes de enviar"""
        statement = select(CustomerNotification).where(
            CustomerNotification.status == "pendiente"
        )
        return db.exec(statement).all()


# Instancias globales - CAJA
cash_register = CRUDCashRegister(CashRegister)
cash_register_session = CRUDCashRegisterSession(CashRegisterSession)
payment_method = CRUDPaymentMethod(PaymentMethod)
cash_transaction = CRUDCashTransaction(CashTransaction)
sale_payment = CRUDSalePayment(SalePayment)
cash_count = CRUDCashCount(CashCount)
cash_count_detail = CRUDCashCountDetail(CashCountDetail)

# Instancias globales - CLIENTES
customer = CRUDCustomer(Customer)
customer_preference = CRUDCustomerPreference(CustomerPreference)
loyalty_transaction = CRUDLoyaltyTransaction(LoyaltyTransaction)
customer_notification = CRUDCustomerNotification(CustomerNotification)
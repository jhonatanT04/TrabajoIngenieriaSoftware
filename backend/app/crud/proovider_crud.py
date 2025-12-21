from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from models.models import (
    Supplier, PurchaseOrder, PurchaseOrderDetail, CreditNote, OrderStatus
)
from .base_crud import CRUDBase


class CRUDSupplier(CRUDBase[Supplier, Supplier, Supplier]):
    def get_by_tax_id(self, db: Session, *, tax_id: str) -> Optional[Supplier]:
        """Obtener proveedor por RUC/Cédula"""
        statement = select(Supplier).where(Supplier.tax_id == tax_id)
        return db.exec(statement).first()
    
    def get_active_suppliers(self, db: Session) -> List[Supplier]:
        """Obtener proveedores activos"""
        statement = select(Supplier).where(Supplier.is_active == True)
        return db.exec(statement).all()
    
    def search_by_name(self, db: Session, *, name: str) -> List[Supplier]:
        """Buscar proveedores por nombre"""
        statement = select(Supplier).where(Supplier.business_name.contains(name))
        return db.exec(statement).all()
    
    def deactivate(self, db: Session, *, id: UUID) -> Supplier:
        """Desactivar proveedor"""
        supplier = self.get(db, id)
        supplier.is_active = False
        supplier.updated_at = datetime.utcnow()
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier


class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrder, PurchaseOrder]):
    def get_by_order_number(self, db: Session, *, order_number: str) -> Optional[PurchaseOrder]:
        """Obtener orden por número"""
        statement = select(PurchaseOrder).where(
            PurchaseOrder.order_number == order_number
        )
        return db.exec(statement).first()
    
    def get_by_supplier(self, db: Session, *, supplier_id: UUID) -> List[PurchaseOrder]:
        """Obtener órdenes de un proveedor"""
        statement = select(PurchaseOrder).where(
            PurchaseOrder.supplier_id == supplier_id
        )
        return db.exec(statement).all()
    
    def get_by_status(self, db: Session, *, status: OrderStatus) -> List[PurchaseOrder]:
        """Obtener órdenes por estado"""
        statement = select(PurchaseOrder).where(PurchaseOrder.status == status)
        return db.exec(statement).all()
    
    def get_pending_orders(self, db: Session) -> List[PurchaseOrder]:
        """Obtener órdenes pendientes"""
        return self.get_by_status(db, status=OrderStatus.pendiente)
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[PurchaseOrder]:
        """Obtener órdenes en un rango de fechas"""
        statement = select(PurchaseOrder).where(
            PurchaseOrder.order_date >= start_date,
            PurchaseOrder.order_date <= end_date
        )
        return db.exec(statement).all()
    
    def update_status(
        self, 
        db: Session, 
        *, 
        id: UUID, 
        status: OrderStatus
    ) -> PurchaseOrder:
        """Actualizar estado de orden"""
        order = self.get(db, id)
        order.status = status
        order.updated_at = datetime.utcnow()
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
    def get_with_details(self, db: Session, *, id: UUID) -> Optional[PurchaseOrder]:
        """Obtener orden con sus detalles"""
        order = self.get(db, id)
        if order:
            _ = order.details  # Carga la relación
        return order


class CRUDPurchaseOrderDetail(CRUDBase[PurchaseOrderDetail, PurchaseOrderDetail, PurchaseOrderDetail]):
    def get_by_order(self, db: Session, *, order_id: UUID) -> List[PurchaseOrderDetail]:
        """Obtener detalles de una orden"""
        statement = select(PurchaseOrderDetail).where(
            PurchaseOrderDetail.purchase_order_id == order_id
        )
        return db.exec(statement).all()
    
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[PurchaseOrderDetail]:
        """Obtener órdenes que incluyen un producto"""
        statement = select(PurchaseOrderDetail).where(
            PurchaseOrderDetail.product_id == product_id
        )
        return db.exec(statement).all()


class CRUDCreditNote(CRUDBase[CreditNote, CreditNote, CreditNote]):
    def get_by_note_number(self, db: Session, *, note_number: str) -> Optional[CreditNote]:
        """Obtener nota de crédito por número"""
        statement = select(CreditNote).where(CreditNote.note_number == note_number)
        return db.exec(statement).first()
    
    def get_by_supplier(self, db: Session, *, supplier_id: UUID) -> List[CreditNote]:
        """Obtener notas de crédito de un proveedor"""
        statement = select(CreditNote).where(CreditNote.supplier_id == supplier_id)
        return db.exec(statement).all()
    
    def get_by_purchase_order(self, db: Session, *, order_id: UUID) -> List[CreditNote]:
        """Obtener notas de crédito de una orden"""
        statement = select(CreditNote).where(
            CreditNote.purchase_order_id == order_id
        )
        return db.exec(statement).all()


# Instancias globales
supplier = CRUDSupplier(Supplier)
purchase_order = CRUDPurchaseOrder(PurchaseOrder)
purchase_order_detail = CRUDPurchaseOrderDetail(PurchaseOrderDetail)
credit_note = CRUDCreditNote(CreditNote)
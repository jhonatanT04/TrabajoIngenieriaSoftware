from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from models.models import (
    Sale, SaleDetail, Promotion, Invoice, SaleStatus, PromotionType
)
from .base_crud import CRUDBase


class CRUDSale(CRUDBase[Sale, Sale, Sale]):
    def get_by_sale_number(self, db: Session, *, sale_number: str) -> Optional[Sale]:
        """Obtener venta por número"""
        statement = select(Sale).where(Sale.sale_number == sale_number)
        return db.exec(statement).first()
    
    def get_by_cashier(self, db: Session, *, cashier_id: UUID) -> List[Sale]:
        """Obtener ventas de un cajero"""
        statement = select(Sale).where(Sale.cashier_id == cashier_id)
        return db.exec(statement).all()
    
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[Sale]:
        """Obtener ventas de un cliente"""
        statement = select(Sale).where(Sale.customer_id == customer_id)
        return db.exec(statement).all()
    
    def get_by_cash_register(self, db: Session, *, cash_register_id: UUID) -> List[Sale]:
        """Obtener ventas de una caja registradora"""
        statement = select(Sale).where(Sale.cash_register_id == cash_register_id)
        return db.exec(statement).all()
    
    def get_by_status(self, db: Session, *, status: SaleStatus) -> List[Sale]:
        """Obtener ventas por estado"""
        statement = select(Sale).where(Sale.status == status)
        return db.exec(statement).all()
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Sale]:
        """Obtener ventas en un rango de fechas"""
        statement = select(Sale).where(
            Sale.sale_date >= start_date,
            Sale.sale_date <= end_date
        )
        return db.exec(statement).all()
    
    def get_today_sales(self, db: Session) -> List[Sale]:
        """Obtener ventas del día"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
        return self.get_by_date_range(db, start_date=today_start, end_date=today_end)
    
    def get_with_details(self, db: Session, *, id: UUID) -> Optional[Sale]:
        """Obtener venta con sus detalles"""
        sale = self.get(db, id)
        if sale:
            _ = sale.details
            _ = sale.payments
        return sale
    
    def cancel_sale(self, db: Session, *, id: UUID) -> Sale:
        """Cancelar una venta"""
        sale = self.get(db, id)
        sale.status = SaleStatus.cancelada
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale
    
    def get_total_sales_amount(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> float:
        """Obtener el monto total de ventas en un periodo"""
        sales = self.get_by_date_range(db, start_date=start_date, end_date=end_date)
        completed_sales = [s for s in sales if s.status == SaleStatus.completada]
        return sum(s.total_amount for s in completed_sales)


class CRUDSaleDetail(CRUDBase[SaleDetail, SaleDetail, SaleDetail]):
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> List[SaleDetail]:
        """Obtener detalles de una venta"""
        statement = select(SaleDetail).where(SaleDetail.sale_id == sale_id)
        return db.exec(statement).all()
    
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[SaleDetail]:
        """Obtener ventas que incluyen un producto"""
        statement = select(SaleDetail).where(SaleDetail.product_id == product_id)
        return db.exec(statement).all()
    
    def get_best_selling_products(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime,
        limit: int = 10
    ) -> List[tuple]:
        """Obtener productos más vendidos en un periodo"""
        # Esta consulta requiere agregación SQL avanzada
        # Se implementaría con select específico o raw SQL
        # Por ahora retornamos estructura básica
        statement = select(SaleDetail)
        details = db.exec(statement).all()
        # Implementar lógica de agrupación y ordenamiento
        return []


class CRUDPromotion(CRUDBase[Promotion, Promotion, Promotion]):
    def get_active_promotions(self, db: Session) -> List[Promotion]:
        """Obtener promociones activas"""
        now = datetime.utcnow()
        statement = select(Promotion).where(
            Promotion.is_active == True,
            Promotion.start_date <= now,
            Promotion.end_date >= now
        )
        return db.exec(statement).all()
    
    def get_by_type(self, db: Session, *, promotion_type: PromotionType) -> List[Promotion]:
        """Obtener promociones por tipo"""
        statement = select(Promotion).where(Promotion.promotion_type == promotion_type)
        return db.exec(statement).all()
    
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[Promotion]:
        """Obtener promociones que aplican a un producto"""
        # Requiere join con la tabla de relación
        statement = select(Promotion)
        promotions = db.exec(statement).all()
        # Filtrar las que incluyen el producto
        return [p for p in promotions if any(prod.id == product_id for prod in p.products)]
    
    def deactivate(self, db: Session, *, id: UUID) -> Promotion:
        """Desactivar promoción"""
        promotion = self.get(db, id)
        promotion.is_active = False
        db.add(promotion)
        db.commit()
        db.refresh(promotion)
        return promotion


class CRUDInvoice(CRUDBase[Invoice, Invoice, Invoice]):
    def get_by_invoice_number(self, db: Session, *, invoice_number: str) -> Optional[Invoice]:
        """Obtener factura por número"""
        statement = select(Invoice).where(Invoice.invoice_number == invoice_number)
        return db.exec(statement).first()
    
    def get_by_sale(self, db: Session, *, sale_id: UUID) -> Optional[Invoice]:
        """Obtener factura de una venta"""
        statement = select(Invoice).where(Invoice.sale_id == sale_id)
        return db.exec(statement).first()
    
    def get_by_customer(self, db: Session, *, customer_id: UUID) -> List[Invoice]:
        """Obtener facturas de un cliente"""
        statement = select(Invoice).where(Invoice.customer_id == customer_id)
        return db.exec(statement).all()
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Invoice]:
        """Obtener facturas en un rango de fechas"""
        statement = select(Invoice).where(
            Invoice.invoice_date >= start_date,
            Invoice.invoice_date <= end_date
        )
        return db.exec(statement).all()
    
    def cancel_invoice(self, db: Session, *, id: UUID) -> Invoice:
        """Anular factura"""
        invoice = self.get(db, id)
        invoice.status = "anulada"
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice


# Instancias globales
sale = CRUDSale(Sale)
sale_detail = CRUDSaleDetail(SaleDetail)
promotion = CRUDPromotion(Promotion)
invoice = CRUDInvoice(Invoice)
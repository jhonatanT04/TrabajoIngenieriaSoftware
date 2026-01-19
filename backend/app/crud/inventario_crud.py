from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from app.models.models import (
    Inventory, Location, InventoryMovement, ProductReception,
    ProductReceptionDetail, ProductLabel, MovementType
)
from .base_crud import CRUDBase


class CRUDInventory(CRUDBase[Inventory, Inventory, Inventory]):
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[Inventory]:
        """Obtener inventario de un producto"""
        statement = select(Inventory).where(Inventory.product_id == product_id)
        return db.exec(statement).all()
    
    def get_by_location(self, db: Session, *, location_id: UUID) -> List[Inventory]:
        """Obtener inventario en una ubicación"""
        statement = select(Inventory).where(Inventory.location_id == location_id)
        return db.exec(statement).all()
    
    def get_product_in_location(
        self, 
        db: Session, 
        *, 
        product_id: UUID, 
        location_id: UUID
    ) -> Optional[Inventory]:
        """Obtener inventario de un producto en una ubicación específica"""
        statement = select(Inventory).where(
            Inventory.product_id == product_id,
            Inventory.location_id == location_id
        )
        return db.exec(statement).first()
    
    def update_stock(
        self, 
        db: Session, 
        *, 
        product_id: UUID, 
        location_id: Optional[UUID],
        quantity: float,
        user_id: UUID
    ) -> Inventory:
        """Actualizar stock de un producto"""
        inventory = self.get_product_in_location(
            db, 
            product_id=product_id, 
            location_id=location_id
        )
        
        if inventory:
            inventory.quantity = quantity
            inventory.last_updated = datetime.utcnow()
            inventory.updated_by = user_id
            db.add(inventory)
        else:
            inventory = Inventory(
                product_id=product_id,
                location_id=location_id,
                quantity=quantity,
                updated_by=user_id
            )
            db.add(inventory)
        
        db.commit()
        db.refresh(inventory)
        return inventory
    
    def get_total_stock_by_product(self, db: Session, *, product_id: UUID) -> float:
        """Obtener stock total de un producto (todas las ubicaciones)"""
        inventories = self.get_by_product(db, product_id=product_id)
        return sum(inv.quantity for inv in inventories)


class CRUDLocation(CRUDBase[Location, Location, Location]):
    def get_by_aisle_and_shelf(
        self, 
        db: Session, 
        *, 
        aisle: str, 
        shelf: str
    ) -> Optional[Location]:
        """Obtener ubicación por pasillo y estante"""
        statement = select(Location).where(
            Location.aisle == aisle,
            Location.shelf == shelf
        )
        return db.exec(statement).first()
    
    def get_by_aisle(self, db: Session, *, aisle: str) -> List[Location]:
        """Obtener todas las ubicaciones de un pasillo"""
        statement = select(Location).where(Location.aisle == aisle)
        return db.exec(statement).all()


class CRUDInventoryMovement(CRUDBase[InventoryMovement, InventoryMovement, InventoryMovement]):
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[InventoryMovement]:
        """Obtener movimientos de un producto"""
        statement = select(InventoryMovement).where(
            InventoryMovement.product_id == product_id
        ).order_by(InventoryMovement.created_at.desc())
        return db.exec(statement).all()
    
    def get_by_type(self, db: Session, *, movement_type: MovementType) -> List[InventoryMovement]:
        """Obtener movimientos por tipo"""
        statement = select(InventoryMovement).where(
            InventoryMovement.movement_type == movement_type
        )
        return db.exec(statement).all()
    
    def get_by_user(self, db: Session, *, user_id: UUID) -> List[InventoryMovement]:
        """Obtener movimientos realizados por un usuario"""
        statement = select(InventoryMovement).where(
            InventoryMovement.user_id == user_id
        )
        return db.exec(statement).all()
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[InventoryMovement]:
        """Obtener movimientos en un rango de fechas"""
        statement = select(InventoryMovement).where(
            InventoryMovement.created_at >= start_date,
            InventoryMovement.created_at <= end_date
        )
        return db.exec(statement).all()
    
    def create_movement(
        self,
        db: Session,
        *,
        product_id: UUID,
        movement_type: MovementType,
        quantity: float,
        previous_stock: float,
        new_stock: float,
        user_id: UUID,
        reason: Optional[str] = None,
        reference_document: Optional[str] = None
    ) -> InventoryMovement:
        """Crear un movimiento de inventario"""
        movement = InventoryMovement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            reason=reason,
            reference_document=reference_document,
            user_id=user_id
        )
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement


class CRUDProductReception(CRUDBase[ProductReception, ProductReception, ProductReception]):
    def get_by_reception_number(
        self, 
        db: Session, 
        *, 
        reception_number: str
    ) -> Optional[ProductReception]:
        """Obtener recepción por número"""
        statement = select(ProductReception).where(
            ProductReception.reception_number == reception_number
        )
        return db.exec(statement).first()
    
    def get_by_purchase_order(
        self, 
        db: Session, 
        *, 
        order_id: UUID
    ) -> List[ProductReception]:
        """Obtener recepciones de una orden de compra"""
        statement = select(ProductReception).where(
            ProductReception.purchase_order_id == order_id
        )
        return db.exec(statement).all()
    
    def get_by_date_range(
        self, 
        db: Session, 
        *, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[ProductReception]:
        """Obtener recepciones en un rango de fechas"""
        statement = select(ProductReception).where(
            ProductReception.reception_date >= start_date,
            ProductReception.reception_date <= end_date
        )
        return db.exec(statement).all()
    
    def get_with_details(self, db: Session, *, id: UUID) -> Optional[ProductReception]:
        """Obtener recepción con sus detalles"""
        reception = self.get(db, id)
        if reception:
            _ = reception.details
        return reception


class CRUDProductReceptionDetail(CRUDBase[ProductReceptionDetail, ProductReceptionDetail, ProductReceptionDetail]):
    def get_by_reception(self, db: Session, *, reception_id: UUID) -> List[ProductReceptionDetail]:
        """Obtener detalles de una recepción"""
        statement = select(ProductReceptionDetail).where(
            ProductReceptionDetail.reception_id == reception_id
        )
        return db.exec(statement).all()
    
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[ProductReceptionDetail]:
        """Obtener recepciones que incluyen un producto"""
        statement = select(ProductReceptionDetail).where(
            ProductReceptionDetail.product_id == product_id
        )
        return db.exec(statement).all()
    
    def get_by_lot(self, db: Session, *, lot_number: str) -> List[ProductReceptionDetail]:
        """Obtener productos por número de lote"""
        statement = select(ProductReceptionDetail).where(
            ProductReceptionDetail.lot_number == lot_number
        )
        return db.exec(statement).all()


class CRUDProductLabel(CRUDBase[ProductLabel, ProductLabel, ProductLabel]):
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[ProductLabel]:
        """Obtener etiquetas de un producto"""
        statement = select(ProductLabel).where(
            ProductLabel.product_id == product_id
        ).order_by(ProductLabel.printed_at.desc())
        return db.exec(statement).all()
    
    def get_by_barcode(self, db: Session, *, barcode: str) -> List[ProductLabel]:
        """Obtener etiquetas por código de barras"""
        statement = select(ProductLabel).where(ProductLabel.barcode == barcode)
        return db.exec(statement).all()


# Instancias globales
inventory = CRUDInventory(Inventory)
location = CRUDLocation(Location)
inventory_movement = CRUDInventoryMovement(InventoryMovement)
product_reception = CRUDProductReception(ProductReception)
product_reception_detail = CRUDProductReceptionDetail(ProductReceptionDetail)
product_label = CRUDProductLabel(ProductLabel)
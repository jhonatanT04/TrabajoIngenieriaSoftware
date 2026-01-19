from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID

from app.models.models import (
    Product, Category, Brand, ProductPresentation
)
from .base_crud import CRUDBase


class CRUDProduct(CRUDBase[Product, Product, Product]):
    def get_by_sku(self, db: Session, *, sku: str) -> Optional[Product]:
        """Obtener producto por SKU"""
        statement = select(Product).where(Product.sku == sku)
        return db.exec(statement).first()
    
    def get_by_barcode(self, db: Session, *, barcode: str) -> Optional[Product]:
        """Obtener producto por código de barras"""
        statement = select(Product).where(Product.barcode == barcode)
        return db.exec(statement).first()
    
    def search_by_name(self, db: Session, *, name: str) -> List[Product]:
        """Buscar productos por nombre (parcial)"""
        statement = select(Product).where(Product.name.contains(name))
        return db.exec(statement).all()
    
    def get_by_category(self, db: Session, *, category_id: UUID) -> List[Product]:
        """Obtener productos por categoría"""
        statement = select(Product).where(Product.category_id == category_id)
        return db.exec(statement).all()
    
    def get_by_supplier(self, db: Session, *, supplier_id: UUID) -> List[Product]:
        """Obtener productos por proveedor"""
        statement = select(Product).where(Product.main_supplier_id == supplier_id)
        return db.exec(statement).all()
    
    def get_low_stock(self, db: Session) -> List[Product]:
        """Obtener productos con stock bajo (menos que stock_min)"""
        statement = select(Product).where(Product.stock_min > 0)
        products = db.exec(statement).all()
        # Filtrar productos donde stock actual < stock_min
        # Nota: necesitarás calcular el stock actual desde la tabla inventory
        return products
    
    def get_active_products(self, db: Session) -> List[Product]:
        """Obtener productos activos"""
        statement = select(Product).where(Product.is_active == True)
        return db.exec(statement).all()
    
    def deactivate(self, db: Session, *, id: UUID) -> Product:
        """Desactivar producto"""
        product = self.get(db, id)
        product.is_active = False
        db.add(product)
        db.commit()
        db.refresh(product)
        return product


class CRUDCategory(CRUDBase[Category, Category, Category]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Category]:
        """Obtener categoría por nombre"""
        statement = select(Category).where(Category.name == name)
        return db.exec(statement).first()
    
    def get_root_categories(self, db: Session) -> List[Category]:
        """Obtener categorías raíz (sin padre)"""
        statement = select(Category).where(Category.parent_category_id == None)
        return db.exec(statement).all()
    
    def get_subcategories(self, db: Session, *, parent_id: UUID) -> List[Category]:
        """Obtener subcategorías de una categoría"""
        statement = select(Category).where(Category.parent_category_id == parent_id)
        return db.exec(statement).all()


class CRUDBrand(CRUDBase[Brand, Brand, Brand]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Brand]:
        """Obtener marca por nombre"""
        statement = select(Brand).where(Brand.name == name)
        return db.exec(statement).first()


class CRUDProductPresentation(CRUDBase[ProductPresentation, ProductPresentation, ProductPresentation]):
    def get_by_product(self, db: Session, *, product_id: UUID) -> List[ProductPresentation]:
        """Obtener presentaciones de un producto"""
        statement = select(ProductPresentation).where(
            ProductPresentation.product_id == product_id
        )
        return db.exec(statement).all()
    
    def get_by_barcode(self, db: Session, *, barcode: str) -> Optional[ProductPresentation]:
        """Obtener presentación por código de barras"""
        statement = select(ProductPresentation).where(
            ProductPresentation.barcode == barcode
        )
        return db.exec(statement).first()


# Instancias globales
product = CRUDProduct(Product)
category = CRUDCategory(Category)
brand = CRUDBrand(Brand)
product_presentation = CRUDProductPresentation(ProductPresentation)
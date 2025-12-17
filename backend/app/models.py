from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime


class Role(str, Enum):
    admin = "admin"
    cashier = "cashier"
    stock = "stock"
    accountant = "accountant"


class UserBase(SQLModel):
    username: str
    full_name: Optional[str] = None
    role: Role = Role.cashier


class User(UserBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = True


class Supplier(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    ruc: str
    name: str
    contact: Optional[str]


class Product(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sku: str = Field(index=True)
    name: str
    category: Optional[str]
    brand: Optional[str]
    supplier_id: Optional[UUID] = Field(default=None, foreign_key="supplier.id")
    content: Optional[str]
    unit: Optional[str]
    price_sale: float = 0.0
    price_cost: float = 0.0
    tax: float = 0.0
    stock: float = 0.0
    stock_min: Optional[float] = 0.0
    stock_max: Optional[float] = None


class InventoryMovement(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="product.id")
    quantity: float
    reason: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None


class Customer(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    document: Optional[str]
    contact: Optional[str]


class SaleItem(SQLModel):
    product_id: UUID
    quantity: float
    price: float


class Sale(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    customer_id: Optional[UUID] = Field(default=None, foreign_key="customer.id")
    total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    items: Optional[List[SaleItem]] = None

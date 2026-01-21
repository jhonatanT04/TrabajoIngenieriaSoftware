from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_name: str
    is_active: bool = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    id: UUID
    username: str
    full_name: Optional[str]
    role: str


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: Optional[str]
    brand: Optional[str]
    price_sale: float = 0.0
    price_cost: float = 0.0
    tax: float = 0.0
    stock: float = 0.0


class ProductRead(ProductCreate):
    id: UUID


class InventoryMovementCreate(BaseModel):
    product_id: UUID
    quantity: float
    reason: Optional[str]


class SaleItemCreate(BaseModel):
    product_id: UUID
    quantity: float
    price: float


class SaleCreate(BaseModel):
    customer_id: Optional[UUID]
    items: List[SaleItemCreate]

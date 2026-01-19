
from typing import Optional
from app.models.enums import *
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime

class ProfilePermission(SQLModel, table=True):
    __tablename__ = "profile_permissions"
    profile_id: UUID = Field(foreign_key="profiles.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permissions.id", primary_key=True)


class PromotionProduct(SQLModel, table=True):
    __tablename__ = "promotion_products"
    promotion_id: UUID = Field(foreign_key="promotions.id", primary_key=True)
    product_id: UUID = Field(foreign_key="products.id", primary_key=True)


class PromotionCategory(SQLModel, table=True):
    __tablename__ = "promotion_categories"
    promotion_id: UUID = Field(foreign_key="promotions.id", primary_key=True)
    category_id: UUID = Field(foreign_key="categories.id", primary_key=True)


# ==================== MÓDULO DE USUARIOS Y CONFIGURACIÓN ====================
class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    users: list["User"] = Relationship(back_populates="profile")
    permissions: list["Permission"] = Relationship(back_populates="profiles", link_model=ProfilePermission)


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    module_name: str
    action: str  # CREATE, READ, UPDATE, DELETE
    description: Optional[str] = None
    
    profiles: list["Profile"] = Relationship(back_populates="permissions", link_model=ProfilePermission)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    profile_id: UUID = Field(foreign_key="profiles.id")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    document_number: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    profile: Optional["Profile"] = Relationship(back_populates="users")
    purchase_orders: list["PurchaseOrder"] = Relationship(back_populates="created_by_user")
    inventory_movements: list["InventoryMovement"] = Relationship(back_populates="user")
    cash_sessions: list["CashRegisterSession"] = Relationship(back_populates="user")
    sales: list["Sale"] = Relationship(back_populates="cashier")


class SystemParameter(SQLModel, table=True):
    __tablename__ = "system_parameters"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    parameter_key: str = Field(unique=True, index=True)
    parameter_value: str
    description: Optional[str] = None
    data_type: str = "string"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[UUID] = Field(default=None, foreign_key="users.id")


# ==================== MÓDULO DE PRODUCTOS ====================
class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    products: list["Product"] = Relationship(back_populates="category")
    promotions: list["Promotion"] = Relationship(back_populates="categories", link_model=PromotionCategory)


class Brand(SQLModel, table=True):
    __tablename__ = "brands"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None

    products: list["Product"] = Relationship(back_populates="brand")


class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sku: str = Field(unique=True, index=True)
    barcode: Optional[str] = Field(default=None, index=True)
    name: str
    description: Optional[str] = None
    category_id: Optional[UUID] = Field(default=None, foreign_key="categories.id")
    brand_id: Optional[UUID] = Field(default=None, foreign_key="brands.id")
    main_supplier_id: Optional[UUID] = Field(default=None, foreign_key="suppliers.id")
    unit_of_measure: str = "unidad"
    sale_price: float = 0.0
    cost_price: float = 0.0
    tax_rate: float = 0.0
    stock_min: float = 0.0
    stock_max: Optional[float] = None
    weight: Optional[float] = None
    requires_lot_control: bool = False
    requires_expiration_date: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    category: Optional["Category"] = Relationship(back_populates="products")
    brand: Optional["Brand"] = Relationship(back_populates="products")
    supplier: Optional["Supplier"] = Relationship(back_populates="products")
    presentations: list["ProductPresentation"] = Relationship(back_populates="product")
    inventory: list["Inventory"] = Relationship(back_populates="product")
    inventory_movements: list["InventoryMovement"] = Relationship(back_populates="product")
    purchase_order_details: list["PurchaseOrderDetail"] = Relationship(back_populates="product")
    reception_details: list["ProductReceptionDetail"] = Relationship(back_populates="product")
    sale_details: list["SaleDetail"] = Relationship(back_populates="product")
    promotions: list["Promotion"] = Relationship(back_populates="products", link_model=PromotionProduct)


class ProductPresentation(SQLModel, table=True):
    __tablename__ = "product_presentations"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    presentation_name: str
    quantity_per_unit: float
    barcode: Optional[str] = None
    price: float
    
    product: Optional["Product"] = Relationship(back_populates="presentations")


# ==================== MÓDULO DE PROVEEDORES ====================
class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    tax_id: str = Field(unique=True, index=True)
    business_name: str
    representative_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_days: Optional[int] = None
    carrier: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    products: list["Product"] = Relationship(back_populates="supplier")
    purchase_orders: list["PurchaseOrder"] = Relationship(back_populates="supplier")
    credit_notes: list["CreditNote"] = Relationship(back_populates="supplier")


class PurchaseOrder(SQLModel, table=True):
    __tablename__ = "purchase_orders"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    order_number: str = Field(unique=True, index=True)
    supplier_id: UUID = Field(foreign_key="suppliers.id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    expected_delivery_date: Optional[datetime] = None
    status: OrderStatus = OrderStatus.pendiente
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    notes: Optional[str] = None
    created_by: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    supplier: Optional["Supplier"] = Relationship(back_populates="purchase_orders")
    created_by_user: Optional["User"] = Relationship(back_populates="purchase_orders")
    details: list["PurchaseOrderDetail"] = Relationship(back_populates="purchase_order")
    receptions: list["ProductReception"] = Relationship(back_populates="purchase_order")
    credit_notes: list["CreditNote"] = Relationship(back_populates="purchase_order")


class PurchaseOrderDetail(SQLModel, table=True):
    __tablename__ = "purchase_order_details"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    purchase_order_id: UUID = Field(foreign_key="purchase_orders.id")
    product_id: UUID = Field(foreign_key="products.id")
    quantity: float
    unit_price: float
    subtotal: float
    
    purchase_order: Optional["PurchaseOrder"] = Relationship(back_populates="details")
    product: Optional["Product"] = Relationship(back_populates="purchase_order_details")


class CreditNote(SQLModel, table=True):
    __tablename__ = "credit_notes"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    supplier_id: UUID = Field(foreign_key="suppliers.id")
    purchase_order_id: Optional[UUID] = Field(default=None, foreign_key="purchase_orders.id")
    note_number: str = Field(unique=True, index=True)
    date: datetime = Field(default_factory=datetime.utcnow)
    amount: float
    reason: Optional[str] = None
    status: str = "activa"
    
    supplier: Optional["Supplier"] = Relationship(back_populates="credit_notes")
    purchase_order: Optional["PurchaseOrder"] = Relationship(back_populates="credit_notes")


# ==================== MÓDULO DE INVENTARIO ====================
class Location(SQLModel, table=True):
    __tablename__ = "locations"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    aisle: str
    shelf: str
    position: Optional[str] = None
    description: Optional[str] = None

    inventory: list["Inventory"] = Relationship(back_populates="location")
    reception_details: list["ProductReceptionDetail"] = Relationship(back_populates="location")


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    location_id: Optional[UUID] = Field(default=None, foreign_key="locations.id")
    quantity: float = 0.0
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[UUID] = Field(default=None, foreign_key="users.id")
    
    product: Optional["Product"] = Relationship(back_populates="inventory")
    location: Optional["Location"] = Relationship(back_populates="inventory")


class InventoryMovement(SQLModel, table=True):
    __tablename__ = "inventory_movements"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    movement_type: MovementType
    quantity: float
    previous_stock: float
    new_stock: float
    reason: Optional[str] = None
    reference_document: Optional[str] = None
    user_id: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    product: Optional["Product"] = Relationship(back_populates="inventory_movements")
    user: Optional["User"] = Relationship(back_populates="inventory_movements")


class ProductReception(SQLModel, table=True):
    __tablename__ = "product_receptions"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    purchase_order_id: UUID = Field(foreign_key="purchase_orders.id")
    reception_number: str = Field(unique=True, index=True)
    reception_date: datetime = Field(default_factory=datetime.utcnow)
    guide_number: Optional[str] = None
    received_by: UUID = Field(foreign_key="users.id")
    notes: Optional[str] = None
    status: str = "recibida"
    
    purchase_order: Optional["PurchaseOrder"] = Relationship(back_populates="receptions")
    details: list["ProductReceptionDetail"] = Relationship(back_populates="reception")


class ProductReceptionDetail(SQLModel, table=True):
    __tablename__ = "product_reception_details"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    reception_id: UUID = Field(foreign_key="product_receptions.id")
    product_id: UUID = Field(foreign_key="products.id")
    quantity_ordered: float
    quantity_received: float
    lot_number: Optional[str] = None
    expiration_date: Optional[datetime] = None
    location_id: Optional[UUID] = Field(default=None, foreign_key="locations.id")
    
    reception: Optional["ProductReception"] = Relationship(back_populates="details")
    product: Optional["Product"] = Relationship(back_populates="reception_details")
    location: Optional["Location"] = Relationship(back_populates="reception_details")


class ProductLabel(SQLModel, table=True):
    __tablename__ = "product_labels"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id")
    barcode: str
    price: float
    printed_at: datetime = Field(default_factory=datetime.utcnow)
    printed_by: UUID = Field(foreign_key="users.id")


# ==================== MÓDULO DE VENTAS ====================
class Sale(SQLModel, table=True):
    __tablename__ = "sales"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sale_number: str = Field(unique=True, index=True)
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    cashier_id: UUID = Field(foreign_key="users.id")
    cash_register_id: UUID = Field(foreign_key="cash_registers.id")
    customer_id: Optional[UUID] = Field(default=None, foreign_key="customers.id")
    subtotal: float = 0.0
    discount_amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    status: SaleStatus = SaleStatus.completada
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    cashier: Optional["User"] = Relationship(back_populates="sales")
    cash_register: Optional["CashRegister"] = Relationship(back_populates="sales")
    customer: Optional["Customer"] = Relationship(back_populates="sales")
    details: list["SaleDetail"] = Relationship(back_populates="sale")
    payments: list["SalePayment"] = Relationship(back_populates="sale")
    invoice: Optional["Invoice"] = Relationship(back_populates="sale")
    loyalty_transactions: list["LoyaltyTransaction"] = Relationship(back_populates="sale")


class SaleDetail(SQLModel, table=True):
    __tablename__ = "sale_details"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sale_id: UUID = Field(foreign_key="sales.id")
    product_id: UUID = Field(foreign_key="products.id")
    quantity: float
    unit_price: float
    discount_percentage: float = 0.0
    discount_amount: float = 0.0
    subtotal: float
    tax_rate: float
    tax_amount: float
    total: float
    
    sale: Optional["Sale"] = Relationship(back_populates="details")
    product: Optional["Product"] = Relationship(back_populates="sale_details")


class Promotion(SQLModel, table=True):
    __tablename__ = "promotions"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    promotion_type: PromotionType
    start_date: datetime
    end_date: datetime
    discount_percentage: float = 0.0
    discount_amount: float = 0.0
    min_quantity: Optional[float] = None
    max_uses_per_customer: Optional[int] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    products: list["Product"] = Relationship(back_populates="promotions", link_model=PromotionProduct)
    categories: list["Category"] = Relationship(back_populates="promotions", link_model=PromotionCategory)


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    invoice_number: str = Field(unique=True, index=True)
    sale_id: UUID = Field(foreign_key="sales.id", unique=True)
    customer_id: UUID = Field(foreign_key="customers.id")
    invoice_date: datetime = Field(default_factory=datetime.utcnow)
    tax_id: str
    business_name: str
    address: Optional[str] = None
    subtotal: float
    tax_amount: float
    total_amount: float
    electronic_signature: Optional[str] = None
    authorization_number: Optional[str] = None
    status: str = "emitida"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    sale: Optional["Sale"] = Relationship(back_populates="invoice")
    customer: Optional["Customer"] = Relationship(back_populates="invoices")


# ==================== MÓDULO DE CAJA ====================
class CashRegister(SQLModel, table=True):
    __tablename__ = "cash_registers"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    register_number: str = Field(unique=True, index=True)
    location: Optional[str] = None
    is_active: bool = True

    sessions: list["CashRegisterSession"] = Relationship(back_populates="cash_register")
    sales: list["Sale"] = Relationship(back_populates="cash_register")


class CashRegisterSession(SQLModel, table=True):
    __tablename__ = "cash_register_sessions"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    cash_register_id: UUID = Field(foreign_key="cash_registers.id")
    user_id: UUID = Field(foreign_key="users.id")
    opening_date: datetime = Field(default_factory=datetime.utcnow)
    closing_date: Optional[datetime] = None
    opening_amount: float = 0.0
    expected_closing_amount: float = 0.0
    actual_closing_amount: float = 0.0
    difference: float = 0.0
    status: SessionStatus = SessionStatus.abierta
    notes: Optional[str] = None
    
    cash_register: Optional["CashRegister"] = Relationship(back_populates="sessions")
    user: Optional["User"] = Relationship(back_populates="cash_sessions")
    transactions: list["CashTransaction"] = Relationship(back_populates="session")
    cash_counts: list["CashCount"] = Relationship(back_populates="session")


class PaymentMethod(SQLModel, table=True):
    __tablename__ = "payment_methods"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    requires_reference: bool = False
    is_active: bool = True
    
    transactions: list["CashTransaction"] = Relationship(back_populates="payment_method")
    sale_payments: list["SalePayment"] = Relationship(back_populates="payment_method")


class CashTransaction(SQLModel, table=True):
    __tablename__ = "cash_transactions"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="cash_register_sessions.id")
    transaction_type: TransactionType
    amount: float
    payment_method_id: UUID = Field(foreign_key="payment_methods.id")
    reference_number: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: UUID = Field(foreign_key="users.id")
    
    session: Optional["CashRegisterSession"] = Relationship(back_populates="transactions")
    payment_method: Optional["PaymentMethod"] = Relationship(back_populates="transactions")


class SalePayment(SQLModel, table=True):
    __tablename__ = "sale_payments"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sale_id: UUID = Field(foreign_key="sales.id")
    payment_method_id: UUID = Field(foreign_key="payment_methods.id")
    amount: float
    reference_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    sale: Optional["Sale"] = Relationship(back_populates="payments")
    payment_method: Optional["PaymentMethod"] = Relationship(back_populates="sale_payments")


class CashCount(SQLModel, table=True):
    __tablename__ = "cash_counts"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="cash_register_sessions.id")
    count_date: datetime = Field(default_factory=datetime.utcnow)
    counted_by: UUID = Field(foreign_key="users.id")
    expected_amount: float
    counted_amount: float
    difference: float
    notes: Optional[str] = None
    
    session: Optional["CashRegisterSession"] = Relationship(back_populates="cash_counts")
    details: list["CashCountDetail"] = Relationship(back_populates="cash_count")


class CashCountDetail(SQLModel, table=True):
    __tablename__ = "cash_count_details"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    cash_count_id: UUID = Field(foreign_key="cash_counts.id")
    denomination: float
    quantity: int
    total: float
    
    cash_count: Optional["CashCount"] = Relationship(back_populates="details")


# ==================== MÓDULO DE CLIENTES ====================
class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    document_type: Optional[str] = None
    document_number: Optional[str] = Field(default=None, index=True)
    first_name: str
    last_name: str
    business_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    segment: str = "regular"
    loyalty_points: float = 0.0
    notes: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    sales: list["Sale"] = Relationship(back_populates="customer")
    invoices: list["Invoice"] = Relationship(back_populates="customer")
    preferences: list["CustomerPreference"] = Relationship(back_populates="customer")
    loyalty_transactions: list["LoyaltyTransaction"] = Relationship(back_populates="customer")
    notifications: list["CustomerNotification"] = Relationship(back_populates="customer")

class CustomerPreference(SQLModel, table=True):
    __tablename__ = "customer_preferences"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    customer_id: UUID = Field(foreign_key="customers.id")
    product_id: UUID = Field(foreign_key="products.id")
    purchase_frequency: int = 0
    last_purchase_date: Optional[datetime] = None
    
    customer: Optional["Customer"] = Relationship(back_populates="preferences")


class LoyaltyTransaction(SQLModel, table=True):
    __tablename__ = "loyalty_transactions"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    customer_id: UUID = Field(foreign_key="customers.id")
    transaction_type: LoyaltyTransactionType
    points: float
    sale_id: Optional[UUID] = Field(default=None, foreign_key="sales.id")
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    customer: Optional["Customer"] = Relationship(back_populates="loyalty_transactions")
    sale: Optional["Sale"] = Relationship(back_populates="loyalty_transactions")


class CustomerNotification(SQLModel, table=True):
    __tablename__ = "customer_notifications"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    customer_id: UUID = Field(foreign_key="customers.id")
    notification_type: str
    message: str
    sent_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "enviada"
    
    customer: Optional["Customer"] = Relationship(back_populates="notifications")


# ==================== MÓDULO DE AUDITORÍA ====================
class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    action: str
    table_name: str
    record_id: Optional[str] = None
    old_values: Optional[str] = None  # JSON string
    new_values: Optional[str] = None  # JSON string
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
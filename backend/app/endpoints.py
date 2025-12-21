"""
ENDPOINTS COMPLETOS - Todos los módulos del sistema
Incluye: Usuarios, Productos, Inventario, Proveedores, Ventas, Caja, Clientes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from deps import *
from models.models import *
from crud.users_crud import *
from crud.products_crud import *
from crud.inventario_crud import *
from crud.proovider_crud import *
from crud.sale_crud import *
from crud.caja_crud import *
from deps import get_db, DBSession

router = APIRouter()


# ==================== SCHEMAS PARA REQUEST BODY ====================
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    profile_id: Optional[UUID] = None
    is_active: bool = True

class ProductCreate(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    brand_id: Optional[UUID] = None
    cost_price: float
    sale_price: float
    stock_min: float = 0
    stock_max: float = 0
    is_active: bool = True

class CustomerCreate(BaseModel):
    document_number: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[UUID] = None

class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = None


# ========================================
# 🔥 ENDPOINTS MÁS FÁCILES PARA PROBAR
# ========================================

@router.post("/test/category", tags=["🔥 FÁCIL - Empezar aquí"])
async def create_category_simple(
    db: DBSession,
    name: str = Body(..., embed=True)
):
    """
    ✅ ENDPOINT MÁS FÁCIL PARA PROBAR
    Solo necesitas enviar el nombre
    
    Body JSON:
    {
        "name": "Electrónicos"
    }
    """
    from crud.products_crud import category
    
    # Verificar si ya existe
    existing = category.get_by_name(db, name=name)
    if existing:
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    
    new_category = Category(name=name)
    created = category.create(db, obj_in=new_category)
    
    return {
        "message": "Categoría creada exitosamente",
        "category": created
    }


@router.post("/test/brand", tags=["🔥 FÁCIL - Empezar aquí"])
async def create_brand_simple(
    db: DBSession,
    name: str = Body(..., embed=True)
):
    """
    ✅ SEGUNDO ENDPOINT MÁS FÁCIL
    
    Body JSON:
    {
        "name": "Samsung"
    }
    """
    from crud.products_crud import brand
    
    existing = brand.get_by_name(db, name=name)
    if existing:
        raise HTTPException(status_code=400, detail="Marca ya existe")
    
    new_brand = Brand(name=name)
    created = brand.create(db, obj_in=new_brand)
    
    return {
        "message": "Marca creada exitosamente",
        "brand": created
    }


# ========================================
# MÓDULO: USUARIOS 👥
# ========================================

@router.post("/users", tags=["👥 Usuarios"])
async def create_user(
    user_data: UserCreate,
    db: DBSession
):
    """
    Crear nuevo usuario
    
    Body JSON:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "hashed_password": "hashed_password_here",
        "is_active": true
    }
    """
    from crud.users_crud import user
    
    # Verificar si el username ya existe
    existing = user.get_by_username(db, username=user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username ya existe")
    
    # Verificar si el email ya existe
    existing_email = user.get_by_email(db, email=user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email ya existe")
    
    new_user = User(**user_data.dict())
    created = user.create(db, obj_in=new_user)
    
    return {
        "message": "Usuario creado exitosamente",
        "user": created
    }


@router.get("/users", tags=["👥 Usuarios"])
async def list_users(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True)
):
    """Listar usuarios"""
    from crud.users_crud import user
    
    if active_only:
        users = user.get_active_users(db)
    else:
        users = user.get_multi(db, skip=skip, limit=limit)
    
    return users


@router.get("/users/{user_id}", tags=["👥 Usuarios"])
async def get_user(
    user_id: UUID,
    db: DBSession
):
    """Obtener usuario por ID"""
    from crud.users_crud import user
    
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_obj


@router.get("/users/username/{username}", tags=["👥 Usuarios"])
async def get_user_by_username(
    username: str,
    db: DBSession
):
    """Obtener usuario por username"""
    from crud.users_crud import user
    
    user_obj = user.get_by_username(db, username=username)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_obj


@router.put("/users/{user_id}", tags=["👥 Usuarios"])
async def update_user(
    user_id: UUID,
    user_data: UserCreate,
    db: DBSession
):
    """Actualizar usuario"""
    from crud.users_crud import user
    
    existing = user.get(db, id=user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    updated = user.update(db, db_obj=existing, obj_in=user_data.dict())
    return updated


@router.delete("/users/{user_id}", tags=["👥 Usuarios"])
async def deactivate_user(
    user_id: UUID,
    db: DBSession
):
    """Desactivar usuario"""
    from crud.users_crud import user
    
    deactivated = user.deactivate(db, id=user_id)
    return {"message": "Usuario desactivado", "user": deactivated}


# ========================================
# MÓDULO: PRODUCTOS 📦
# ========================================

@router.post("/products", tags=["📦 Productos"])
async def create_product(
    product_data: ProductCreate,
    db: DBSession
):
    """
    Crear nuevo producto
    
    Body JSON:
    {
        "name": "Laptop HP",
        "sku": "LAP-HP-001",
        "barcode": "7891234567890",
        "cost_price": 500.00,
        "sale_price": 750.00,
        "stock_min": 5,
        "stock_max": 50
    }
    """
    from crud.products_crud import product
    
    # Verificar si el SKU ya existe
    existing = product.get_by_sku(db, sku=product_data.sku)
    if existing:
        raise HTTPException(status_code=400, detail="SKU ya existe")
    
    new_product = Product(**product_data.dict())
    created = product.create(db, obj_in=new_product)
    
    return {
        "message": "Producto creado exitosamente",
        "product": created
    }


@router.get("/products", tags=["📦 Productos"])
async def list_products(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True)
):
    """Listar productos"""
    from crud.products_crud import product
    
    if active_only:
        products = product.get_active_products(db)
        return products[skip:skip+limit]
    else:
        return product.get_multi(db, skip=skip, limit=limit)


@router.get("/products/{product_id}", tags=["📦 Productos"])
async def get_product(
    product_id: UUID,
    db: DBSession
):
    """Obtener producto por ID"""
    from crud.products_crud import product
    
    prod = product.get(db, id=product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.get("/products/sku/{sku}", tags=["📦 Productos"])
async def get_product_by_sku(
    sku: str,
    db: DBSession
):
    """Obtener producto por SKU"""
    from crud.products_crud import product
    
    prod = product.get_by_sku(db, sku=sku)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.get("/products/barcode/{barcode}", tags=["📦 Productos"])
async def get_product_by_barcode(
    barcode: str,
    db: DBSession
):
    """Obtener producto por código de barras"""
    from crud.products_crud import product
    
    prod = product.get_by_barcode(db, barcode=barcode)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod


@router.get("/products/search/name", tags=["📦 Productos"])
async def search_products_by_name(
    db: DBSession,
    name: str = Query(..., min_length=1)
):
    """Buscar productos por nombre"""
    from crud.products_crud import product
    
    products = product.search_by_name(db, name=name)
    return products


@router.get("/products/category/{category_id}", tags=["📦 Productos"])
async def get_products_by_category(
    category_id: UUID,
    db: DBSession
):
    """Obtener productos por categoría"""
    from crud.products_crud import product
    
    products = product.get_by_category(db, category_id=category_id)
    return products


@router.get("/products/supplier/{supplier_id}", tags=["📦 Productos"])
async def get_products_by_supplier(
    supplier_id: UUID,
    db: DBSession
):
    """Obtener productos por proveedor"""
    from crud.products_crud import product
    
    products = product.get_by_supplier(db, supplier_id=supplier_id)
    return products


@router.get("/products/low-stock/list", tags=["📦 Productos"])
async def get_low_stock_products(
    db: DBSession
):
    """Obtener productos con stock bajo"""
    from crud.products_crud import product
    
    products = product.get_low_stock(db)
    return products


@router.put("/products/{product_id}", tags=["📦 Productos"])
async def update_product(
    product_id: UUID,
    product_data: ProductCreate,
    db: DBSession
):
    """Actualizar producto"""
    from crud.products_crud import product
    
    existing = product.get(db, id=product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    updated = product.update(db, db_obj=existing, obj_in=product_data.dict())
    return updated


@router.delete("/products/{product_id}", tags=["📦 Productos"])
async def deactivate_product(
    product_id: UUID,
    db: DBSession
):
    """Desactivar producto"""
    from crud.products_crud import product
    
    deactivated = product.deactivate(db, id=product_id)
    return {"message": "Producto desactivado", "product": deactivated}


# ========================================
# MÓDULO: CATEGORÍAS 🏷️
# ========================================

@router.post("/categories", tags=["🏷️ Categorías"])
async def create_category(
    category_data: CategoryCreate,
    db: DBSession
):
    """
    Crear categoría
    
    Body JSON:
    {
        "name": "Electrónica",
        "description": "Productos electrónicos"
    }
    """
    from crud.products_crud import category
    
    existing = category.get_by_name(db, name=category_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    
    new_category = Category(**category_data.dict())
    created = category.create(db, obj_in=new_category)
    
    return {
        "message": "Categoría creada exitosamente",
        "category": created
    }


@router.get("/categories", tags=["🏷️ Categorías"])
async def list_categories(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Listar categorías"""
    from crud.products_crud import category
    
    categories = category.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/categories/root", tags=["🏷️ Categorías"])
async def get_root_categories(
    db: DBSession
):
    """Obtener categorías raíz (sin padre)"""
    from crud.products_crud import category
    
    categories = category.get_root_categories(db)
    return categories


@router.get("/categories/{category_id}/subcategories", tags=["🏷️ Categorías"])
async def get_subcategories(
    category_id: UUID,
    db: DBSession
):
    """Obtener subcategorías"""
    from crud.products_crud import category
    
    subcategories = category.get_subcategories(db, parent_id=category_id)
    return subcategories


# ========================================
# MÓDULO: MARCAS 🏭
# ========================================

@router.post("/brands", tags=["🏭 Marcas"])
async def create_brand(
    brand_data: BrandCreate,
    db: DBSession
):
    """
    Crear marca
    
    Body JSON:
    {
        "name": "Samsung",
        "description": "Marca de electrónicos"
    }
    """
    from crud.products_crud import brand
    
    existing = brand.get_by_name(db, name=brand_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Marca ya existe")
    
    new_brand = Brand(**brand_data.dict())
    created = brand.create(db, obj_in=new_brand)
    
    return {
        "message": "Marca creada exitosamente",
        "brand": created
    }


@router.get("/brands", tags=["🏭 Marcas"])
async def list_brands(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Listar marcas"""
    from crud.products_crud import brand
    
    brands = brand.get_multi(db, skip=skip, limit=limit)
    return brands


@router.get("/brands/{brand_id}", tags=["🏭 Marcas"])
async def get_brand(
    brand_id: UUID,
    db: DBSession
):
    """Obtener marca por ID"""
    from crud.products_crud import brand
    
    brand_obj = brand.get(db, id=brand_id)
    if not brand_obj:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return brand_obj


# ========================================
# MÓDULO: CLIENTES 👨‍💼
# ========================================

@router.post("/customers", tags=["👨‍💼 Clientes"])
async def create_customer(
    customer_data: CustomerCreate,
    db: DBSession
):
    """
    Crear cliente
    
    Body JSON:
    {
        "document_number": "0123456789",
        "first_name": "Juan",
        "last_name": "Pérez",
        "email": "juan@example.com",
        "phone": "0999999999"
    }
    """
    from crud.caja_crud import customer
    
    # Verificar si ya existe
    existing = customer.get_by_document(db, document_number=customer_data.document_number)
    if existing:
        raise HTTPException(status_code=400, detail="Cliente con este documento ya existe")
    
    new_customer = Customer(**customer_data.dict())
    created = customer.create(db, obj_in=new_customer)
    
    return {
        "message": "Cliente creado exitosamente",
        "customer": created
    }


@router.get("/customers", tags=["👨‍💼 Clientes"])
async def list_customers(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True)
):
    """Listar clientes"""
    from crud.caja_crud import customer
    
    if active_only:
        customers = customer.get_active_customers(db)
        return customers[skip:skip+limit]
    else:
        return customer.get_multi(db, skip=skip, limit=limit)


@router.get("/customers/{customer_id}", tags=["👨‍💼 Clientes"])
async def get_customer(
    customer_id: UUID,
    db: DBSession
):
    """Obtener cliente por ID"""
    from crud.caja_crud import customer
    
    cust = customer.get(db, id=customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cust


@router.get("/customers/document/{document_number}", tags=["👨‍💼 Clientes"])
async def get_customer_by_document(
    document_number: str,
    db: DBSession
):
    """Obtener cliente por documento"""
    from crud.caja_crud import customer
    
    cust = customer.get_by_document(db, document_number=document_number)
    if not cust:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cust


@router.get("/customers/search/name", tags=["👨‍💼 Clientes"])
async def search_customers_by_name(
    db: DBSession,
    name: str = Query(..., min_length=2)
):
    """Buscar clientes por nombre"""
    from crud.caja_crud import customer
    
    customers = customer.search_by_name(db, name=name)
    return customers


@router.get("/customers/vip/list", tags=["👨‍💼 Clientes"])
async def get_vip_customers(
    db: DBSession
):
    """Listar clientes VIP"""
    from crud.caja_crud import customer
    
    customers = customer.get_vip_customers(db)
    return customers


@router.get("/customers/top/list", tags=["👨‍💼 Clientes"])
async def get_top_customers(
    db: DBSession,
    limit: int = Query(10, ge=1, le=50)
):
    """Top clientes por puntos"""
    from crud.caja_crud import customer
    
    customers = customer.get_top_customers(db, limit=limit)
    return customers


@router.post("/customers/{customer_id}/loyalty-points", tags=["👨‍💼 Clientes"])
async def update_loyalty_points(
    customer_id: UUID,
    db: DBSession,
    points: float = Body(..., embed=True)
):
    """
    Actualizar puntos de fidelidad
    
    Body JSON:
    {
        "points": 50.0
    }
    """
    from crud.caja_crud import customer
    
    updated = customer.update_loyalty_points(db, id=customer_id, points=points)
    return updated


# ========================================
# MÓDULO: PROVEEDORES 🏢
# ========================================

class SupplierCreate(BaseModel):
    business_name: str
    tax_id: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True


@router.post("/suppliers", tags=["🏢 Proveedores"])
async def create_supplier(
    supplier_data: SupplierCreate,
    db: DBSession
):
    """
    Crear proveedor
    
    Body JSON:
    {
        "business_name": "Distribuidora XYZ",
        "tax_id": "1234567890001",
        "contact_name": "María García",
        "phone": "0999999999",
        "email": "contacto@xyz.com"
    }
    """
    from crud.proovider_crud import supplier
    
    existing = supplier.get_by_tax_id(db, tax_id=supplier_data.tax_id)
    if existing:
        raise HTTPException(status_code=400, detail="Proveedor con este RUC ya existe")
    
    new_supplier = Supplier(**supplier_data.dict())
    created = supplier.create(db, obj_in=new_supplier)
    
    return {
        "message": "Proveedor creado exitosamente",
        "supplier": created
    }


@router.get("/suppliers", tags=["🏢 Proveedores"])
async def list_suppliers(
    db: DBSession,
    active_only: bool = Query(True)
):
    """Listar proveedores"""
    from crud.proovider_crud import supplier
    
    if active_only:
        return supplier.get_active_suppliers(db)
    else:
        return supplier.get_multi(db)


@router.get("/suppliers/{supplier_id}", tags=["🏢 Proveedores"])
async def get_supplier(
    supplier_id: UUID,
    db: DBSession
):
    """Obtener proveedor por ID"""
    from crud.proovider_crud import supplier
    
    supp = supplier.get(db, id=supplier_id)
    if not supp:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return supp


@router.get("/suppliers/search/name", tags=["🏢 Proveedores"])
async def search_suppliers_by_name(
    db: DBSession,
    name: str = Query(..., min_length=2)
):
    """Buscar proveedores por nombre"""
    from crud.proovider_crud import supplier
    
    suppliers = supplier.search_by_name(db, name=name)
    return suppliers


# ========================================
# MÓDULO: INVENTARIO 📊
# ========================================

class InventoryUpdate(BaseModel):
    product_id: UUID
    location_id: Optional[UUID] = None
    quantity: float


@router.post("/inventory/update-stock", tags=["📊 Inventario"])
async def update_inventory_stock(
    data: InventoryUpdate,
    db: DBSession,
    user_id: UUID = Body(...)
):
    """
    Actualizar stock de inventario
    
    Body JSON:
    {
        "product_id": "uuid-here",
        "quantity": 100.0,
        "user_id": "uuid-here"
    }
    """
    from crud.inventario_crud import inventory
    
    updated = inventory.update_stock(
        db,
        product_id=data.product_id,
        location_id=data.location_id,
        quantity=data.quantity,
        user_id=user_id
    )
    
    return {
        "message": "Stock actualizado exitosamente",
        "inventory": updated
    }


@router.get("/inventory/product/{product_id}", tags=["📊 Inventario"])
async def get_product_inventory(
    product_id: UUID,
    db: DBSession
):
    """Obtener inventario de un producto"""
    from crud.inventario_crud import inventory
    
    inventories = inventory.get_by_product(db, product_id=product_id)
    total_stock = inventory.get_total_stock_by_product(db, product_id=product_id)
    
    return {
        "product_id": product_id,
        "total_stock": total_stock,
        "locations": inventories
    }


@router.get("/inventory/location/{location_id}", tags=["📊 Inventario"])
async def get_location_inventory(
    location_id: UUID,
    db: DBSession
):
    """Obtener inventario por ubicación"""
    from crud.inventario_crud import inventory
    
    inventories = inventory.get_by_location(db, location_id=location_id)
    return inventories


# ========================================
# CONTADOR DE ENDPOINTS
# ========================================

@router.get("/info/endpoints-count", tags=["ℹ️ Info"])
async def endpoints_count():
    """Información de endpoints disponibles"""
    return {
        "total_endpoints": 50,
        "modules": {
            "usuarios": 6,
            "productos": 10,
            "categorias": 4,
            "marcas": 3,
            "clientes": 8,
            "proveedores": 4,
            "inventario": 3,
            "test": 2
        },
        "easiest_to_test": [
            "POST /test/category - Solo necesitas un nombre",
            "POST /test/brand - Solo necesitas un nombre",
            "POST /categories - Crear categoría",
            "POST /brands - Crear marca"
        ]
    }
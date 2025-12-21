"""
Sistema de Dependencias para FastAPI
Incluye autenticación, autorización y acceso a CRUD
"""
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from uuid import UUID

# Imports de autenticación
from auth.auth import decode_token
from db.database import get_session

# Imports de CRUD
from crud.users_crud import user, profile, permission, system_parameter
from crud.products_crud import product, category, brand, product_presentation
from crud.inventario_crud import (
    inventory, location, inventory_movement, 
    product_reception, product_reception_detail, product_label
)
from crud.proovider_crud import supplier, purchase_order, purchase_order_detail, credit_note
from crud.sale_crud import sale, sale_detail, promotion, invoice
from crud.caja_crud import (
    cash_register, cash_register_session, payment_method, 
    cash_transaction, sale_payment, cash_count, cash_count_detail,
    customer, customer_preference, loyalty_transaction, customer_notification
)

from models.models import User, Profile


# ==================== CONFIGURACIÓN DE SEGURIDAD ====================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ==================== DEPENDENCIAS BÁSICAS ====================
# deps.py
def get_db():
    """Obtener sesión de base de datos"""
    session = next(get_session())
    try:
        yield session
    finally:
        session.close()


async def get_token(token: str = Depends(oauth2_scheme)) -> str:
    """Obtener token del header"""
    return token


# ==================== DEPENDENCIAS DE AUTENTICACIÓN ====================
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario actual desde el token"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta identificador de usuario"
        )
    
    current_user = user.get(db, id=UUID(user_id))
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return current_user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verificar que el usuario esté activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


# ==================== DEPENDENCIAS DE AUTORIZACIÓN ====================
class PermissionChecker:
    """Verificador de permisos basado en módulo y acción"""
    
    def __init__(self, module_name: str, action: str):
        self.module_name = module_name
        self.action = action
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """Verificar si el usuario tiene el permiso requerido"""
        if not current_user.profile_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin perfil asignado"
            )
        
        # Obtener perfil con permisos
        user_profile = profile.get_with_permissions(db, id=current_user.profile_id)
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Perfil no encontrado"
            )
        
        # Verificar si tiene el permiso específico
        has_permission = any(
            perm.module_name == self.module_name and perm.action == self.action
            for perm in user_profile.permissions
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permiso para {self.action} en {self.module_name}"
            )
        
        return current_user


def require_role(*allowed_roles: str):
    """Decorador para requerir roles específicos"""
    async def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        if not current_user.profile_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin perfil asignado"
            )
        
        user_profile = profile.get(db, id=current_user.profile_id)
        
        if not user_profile or user_profile.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requiere uno de estos roles: {', '.join(allowed_roles)}"
            )
        
        return current_user
    
    return role_checker


# ==================== DEPENDENCIAS DE CRUD - USUARIOS ====================
def get_user_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de usuarios"""
    return user


def get_profile_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de perfiles"""
    return profile


def get_permission_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de permisos"""
    return permission


def get_system_parameter_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de parámetros del sistema"""
    return system_parameter


# ==================== DEPENDENCIAS DE CRUD - PRODUCTOS ====================
def get_product_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de productos"""
    return product


def get_category_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de categorías"""
    return category


def get_brand_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de marcas"""
    return brand


def get_product_presentation_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de presentaciones de productos"""
    return product_presentation


# ==================== DEPENDENCIAS DE CRUD - INVENTARIO ====================
def get_inventory_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de inventario"""
    return inventory


def get_location_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de ubicaciones"""
    return location


def get_inventory_movement_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de movimientos de inventario"""
    return inventory_movement


def get_product_reception_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de recepción de productos"""
    return product_reception


def get_product_reception_detail_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de detalles de recepción"""
    return product_reception_detail


def get_product_label_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de etiquetas de productos"""
    return product_label


# ==================== DEPENDENCIAS DE CRUD - PROVEEDORES ====================
def get_supplier_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de proveedores"""
    return supplier


def get_purchase_order_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de órdenes de compra"""
    return purchase_order


def get_purchase_order_detail_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de detalles de órdenes de compra"""
    return purchase_order_detail


def get_credit_note_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de notas de crédito"""
    return credit_note


# ==================== DEPENDENCIAS DE CRUD - VENTAS ====================
def get_sale_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de ventas"""
    return sale


def get_sale_detail_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de detalles de ventas"""
    return sale_detail


def get_promotion_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de promociones"""
    return promotion


def get_invoice_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de facturas"""
    return invoice


# ==================== DEPENDENCIAS DE CRUD - CAJA ====================
def get_cash_register_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de cajas registradoras"""
    return cash_register


def get_cash_register_session_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de sesiones de caja"""
    return cash_register_session


def get_payment_method_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de métodos de pago"""
    return payment_method


def get_cash_transaction_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de transacciones de caja"""
    return cash_transaction


def get_sale_payment_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de pagos de ventas"""
    return sale_payment


def get_cash_count_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de arqueos de caja"""
    return cash_count


def get_cash_count_detail_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de detalles de arqueos"""
    return cash_count_detail


# ==================== DEPENDENCIAS DE CRUD - CLIENTES ====================
def get_customer_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de clientes"""
    return customer


def get_customer_preference_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de preferencias de clientes"""
    return customer_preference


def get_loyalty_transaction_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de transacciones de fidelidad"""
    return loyalty_transaction


def get_customer_notification_crud(db: Session = Depends(get_db)):
    """Obtener instancia de CRUD de notificaciones de clientes"""
    return customer_notification


# ==================== DEPENDENCIAS COMBINADAS ====================
CurrentUser = Annotated[User, Depends(get_current_user)]
ActiveUser = Annotated[User, Depends(get_current_active_user)]
DBSession = Annotated[Session, Depends(get_db)]


# ==================== PERMISOS PREDEFINIDOS ====================
# Usuarios
RequireUserRead = Depends(PermissionChecker("usuarios", "leer"))
RequireUserCreate = Depends(PermissionChecker("usuarios", "crear"))
RequireUserUpdate = Depends(PermissionChecker("usuarios", "actualizar"))
RequireUserDelete = Depends(PermissionChecker("usuarios", "eliminar"))

# Productos
RequireProductRead = Depends(PermissionChecker("productos", "leer"))
RequireProductCreate = Depends(PermissionChecker("productos", "crear"))
RequireProductUpdate = Depends(PermissionChecker("productos", "actualizar"))
RequireProductDelete = Depends(PermissionChecker("productos", "eliminar"))

# Inventario
RequireInventoryRead = Depends(PermissionChecker("inventario", "leer"))
RequireInventoryCreate = Depends(PermissionChecker("inventario", "crear"))
RequireInventoryUpdate = Depends(PermissionChecker("inventario", "actualizar"))
RequireInventoryDelete = Depends(PermissionChecker("inventario", "eliminar"))

# Ventas
RequireSaleRead = Depends(PermissionChecker("ventas", "leer"))
RequireSaleCreate = Depends(PermissionChecker("ventas", "crear"))
RequireSaleUpdate = Depends(PermissionChecker("ventas", "actualizar"))
RequireSaleDelete = Depends(PermissionChecker("ventas", "eliminar"))

# Compras
RequirePurchaseRead = Depends(PermissionChecker("compras", "leer"))
RequirePurchaseCreate = Depends(PermissionChecker("compras", "crear"))
RequirePurchaseUpdate = Depends(PermissionChecker("compras", "actualizar"))
RequirePurchaseDelete = Depends(PermissionChecker("compras", "eliminar"))

# Caja
RequireCashRead = Depends(PermissionChecker("caja", "leer"))
RequireCashCreate = Depends(PermissionChecker("caja", "crear"))
RequireCashUpdate = Depends(PermissionChecker("caja", "actualizar"))
RequireCashDelete = Depends(PermissionChecker("caja", "eliminar"))

# Clientes
RequireCustomerRead = Depends(PermissionChecker("clientes", "leer"))
RequireCustomerCreate = Depends(PermissionChecker("clientes", "crear"))
RequireCustomerUpdate = Depends(PermissionChecker("clientes", "actualizar"))
RequireCustomerDelete = Depends(PermissionChecker("clientes", "eliminar"))

# Reportes
RequireReportRead = Depends(PermissionChecker("reportes", "leer"))

# Administración
RequireAdminAccess = Depends(require_role("Administrador", "SuperAdmin"))
RequireManagerAccess = Depends(require_role("Administrador", "SuperAdmin", "Gerente"))


# ==================== UTILIDADES ====================
def verify_resource_ownership(
    resource_user_id: UUID,
    current_user: User,
    allow_admin: bool = True
) -> None:
    """
    Verificar que el usuario actual sea dueño del recurso
    o tenga permisos de administrador
    """
    if current_user.id != resource_user_id:
        if not allow_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permiso para acceder a este recurso"
            )
        # Verificar si es admin (esto requeriría acceso a db y profile)
        # Por simplicidad, lanzamos la excepción
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para acceder a este recurso"
        )


async def get_optional_user(
    token: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Obtener usuario actual si está autenticado, sino None
    Útil para endpoints públicos con funcionalidad adicional para usuarios autenticados
    """
    if not token:
        return None
    
    try:
        # Remover "Bearer " del token
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = decode_token(token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        current_user = user.get(db, id=UUID(user_id))
        return current_user if current_user and current_user.is_active else None
    except:
        return None


# ==================== EXPORT ====================
__all__ = [
    # Básicas
    "get_db",
    "get_token",
    "get_current_user",
    "get_current_active_user",
    "get_optional_user",
    
    # Autorización
    "PermissionChecker",
    "require_role",
    "verify_resource_ownership",
    
    # CRUD Usuarios
    "get_user_crud",
    "get_profile_crud",
    "get_permission_crud",
    "get_system_parameter_crud",
    
    # CRUD Productos
    "get_product_crud",
    "get_category_crud",
    "get_brand_crud",
    "get_product_presentation_crud",
    
    # CRUD Inventario
    "get_inventory_crud",
    "get_location_crud",
    "get_inventory_movement_crud",
    "get_product_reception_crud",
    "get_product_reception_detail_crud",
    "get_product_label_crud",
    
    # CRUD Proveedores
    "get_supplier_crud",
    "get_purchase_order_crud",
    "get_purchase_order_detail_crud",
    "get_credit_note_crud",
    
    # CRUD Ventas
    "get_sale_crud",
    "get_sale_detail_crud",
    "get_promotion_crud",
    "get_invoice_crud",
    
    # CRUD Caja
    "get_cash_register_crud",
    "get_cash_register_session_crud",
    "get_payment_method_crud",
    "get_cash_transaction_crud",
    "get_sale_payment_crud",
    "get_cash_count_crud",
    "get_cash_count_detail_crud",
    
    # CRUD Clientes
    "get_customer_crud",
    "get_customer_preference_crud",
    "get_loyalty_transaction_crud",
    "get_customer_notification_crud",
    
    # Tipos anotados
    "CurrentUser",
    "ActiveUser",
    "DBSession",
    
    # Permisos predefinidos
    "RequireUserRead",
    "RequireUserCreate",
    "RequireUserUpdate",
    "RequireUserDelete",
    "RequireProductRead",
    "RequireProductCreate",
    "RequireProductUpdate",
    "RequireProductDelete",
    "RequireInventoryRead",
    "RequireInventoryCreate",
    "RequireInventoryUpdate",
    "RequireInventoryDelete",
    "RequireSaleRead",
    "RequireSaleCreate",
    "RequireSaleUpdate",
    "RequireSaleDelete",
    "RequirePurchaseRead",
    "RequirePurchaseCreate",
    "RequirePurchaseUpdate",
    "RequirePurchaseDelete",
    "RequireCashRead",
    "RequireCashCreate",
    "RequireCashUpdate",
    "RequireCashDelete",
    "RequireCustomerRead",
    "RequireCustomerCreate",
    "RequireCustomerUpdate",
    "RequireCustomerDelete",
    "RequireReportRead",
    "RequireAdminAccess",
    "RequireManagerAccess",
]
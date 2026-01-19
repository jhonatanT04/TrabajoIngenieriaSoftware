"""
Sistema de autenticación JWT completo
Archivo: backend/app/auth.py
"""
from datetime import datetime, timedelta
from typing import Optional, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError
from sqlmodel import Session
from uuid import UUID
from dotenv import load_dotenv
import os

from app.db.database import get_session
from app.models.models import User
from app.crud import users_crud

load_dotenv()

# Configuración
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_TO_A_SECURE_RANDOM_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Contexto de encriptación para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad para FastAPI
security = HTTPBearer()


# ==================== FUNCIONES DE CONTRASEÑA ====================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Obtener hash de contraseña"""
    return pwd_context.hash(password)


# ==================== FUNCIONES DE TOKEN ====================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear token JWT de acceso
    
    Args:
        data: Datos a incluir en el token (generalmente user_id y username)
        expires_delta: Tiempo de expiración personalizado
    
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decodificar token JWT
    
    Args:
        token: Token JWT a decodificar
    
    Returns:
        Payload del token o None si es inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except JWTError:
        return None


# ==================== AUTENTICACIÓN DE USUARIO ====================
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Autenticar usuario con username y password
    
    Args:
        db: Sesión de base de datos
        username: Nombre de usuario o email
        password: Contraseña en texto plano
    
    Returns:
        Usuario autenticado o None
    """
    # Intentar buscar por username
    user = users_crud.user.get_by_username(db, username=username)
    
    # Si no se encuentra, intentar por email
    if not user:
        user = users_crud.user.get_by_email(db, email=username)
    
    # Si no existe el usuario o está inactivo
    if not user or not user.is_active:
        return None
    
    # Verificar contraseña
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


# ==================== DEPENDENCIAS DE FASTAPI ====================
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> User:
    """
    Obtener usuario actual desde el token JWT
    
    Dependency para usar en rutas protegidas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extraer token
        token = credentials.credentials
        
        # Decodificar token
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        
        # Extraer user_id del payload
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except Exception:
        raise credentials_exception
    
    # Obtener usuario de la base de datos
    user = users_crud.user.get(db, id=UUID(user_id))
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Obtener usuario actual activo
    
    Dependency adicional para verificar que el usuario esté activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


# ==================== VERIFICACIÓN DE PERMISOS ====================
class PermissionChecker:
    """
    Clase para verificar permisos de usuario
    """
    def __init__(self, required_permissions: list[str] = None):
        self.required_permissions = required_permissions or []
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_session)
    ) -> User:
        """
        Verificar que el usuario tenga los permisos requeridos
        """
        # Cargar el perfil con sus permisos
        profile = users_crud.profile.get_with_permissions(db, id=current_user.profile_id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Perfil no encontrado"
            )
        
        # Verificar permisos
        user_permissions = [
            f"{perm.module_name}:{perm.action}" 
            for perm in profile.permissions
        ]
        
        for required_perm in self.required_permissions:
            if required_perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permiso requerido: {required_perm}"
                )
        
        return current_user


# ==================== DECORADORES DE ROL ====================
class RoleChecker:
    """
    Clase para verificar roles de usuario
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_session)
    ) -> User:
        """
        Verificar que el usuario tenga uno de los roles permitidos
        """
        profile = users_crud.profile.get(db, id=current_user.profile_id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Perfil no encontrado"
            )
        
        if profile.name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Rol no permitido. Se requiere uno de: {', '.join(self.allowed_roles)}"
            )
        
        return current_user


# ==================== FUNCIONES AUXILIARES ====================
def create_user_token(user: User) -> dict:
    """
    Crear token para un usuario
    
    Returns:
        Dict con access_token y token_type
    """
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def verify_token_valid(token: str) -> bool:
    """
    Verificar si un token es válido
    
    Returns:
        True si es válido, False si no
    """
    payload = decode_token(token)
    return payload is not None
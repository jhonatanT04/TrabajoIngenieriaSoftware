"""
Rutas de autenticación y usuarios
Archivo: backend/app/routers/auth.py
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

from db.database import get_session
from models.models import User, Profile
from crud import crud
from auth.auth import (
    authenticate_user,
    create_user_token,
    get_password_hash,
    get_current_user,
    get_current_active_user,
    RoleChecker,
    verify_password
)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


# ==================== SCHEMAS ====================
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_name: str = "Cajero"  # Perfil por defecto


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    profile_name: str
    
    class Config:
        from_attributes = True


# ==================== ENDPOINTS ====================
@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_session)
):
    """
    Iniciar sesión con username/email y contraseña
    
    Returns:
        Token JWT de acceso y datos del usuario
    """
    # Autenticar usuario
    user = authenticate_user(db, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    token_data = create_user_token(user)
    
    # Obtener nombre del perfil
    profile = crud.profile.get(db, id=user.profile_id)
    
    return {
        **token_data,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_name": profile.name if profile else None
        }
    }


@router.post("/register", response_model=TokenResponse)
def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_session)
):
    """
    Registrar un nuevo usuario
    
    Note: En producción, este endpoint debería estar protegido
    y solo accesible para administradores
    """
    # Verificar si el usuario ya existe
    existing_user = crud.user.get_by_username(db, username=register_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    
    existing_email = crud.user.get_by_email(db, email=register_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Obtener o crear perfil
    profile = crud.profile.get_by_name(db, name=register_data.profile_name)
    if not profile:
        # Crear perfil básico si no existe
        profile = Profile(name=register_data.profile_name)
        profile = crud.profile.create(db, obj_in=profile)
    
    # Crear usuario
    user_data = User(
        username=register_data.username,
        email=register_data.email,
        hashed_password=get_password_hash(register_data.password),
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        profile_id=profile.id,
        is_active=True
    )
    
    user = crud.user.create(db, obj_in=user_data)
    
    # Crear token
    token_data = create_user_token(user)
    
    return {
        **token_data,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_name": profile.name
        }
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Obtener información del usuario actual
    """
    profile = crud.profile.get(db, id=current_user.profile_id)
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        profile_name=profile.name if profile else "Sin perfil"
    )


@router.put("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Cambiar contraseña del usuario actual
    """
    # Verificar contraseña actual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Validar nueva contraseña
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe tener al menos 8 caracteres"
        )
    
    # Actualizar contraseña
    new_hashed_password = get_password_hash(password_data.new_password)
    crud.user.update_password(db, user=current_user, hashed_password=new_hashed_password)
    
    return {"message": "Contraseña actualizada exitosamente"}


@router.post("/refresh")
def refresh_token(
    current_user: User = Depends(get_current_active_user)
):
    """
    Refrescar token de acceso
    """
    token_data = create_user_token(current_user)
    return token_data


# ==================== ENDPOINTS SOLO PARA ADMINISTRADORES ====================
@router.get(
    "/users",
    dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))]
)
def list_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Listar todos los usuarios (solo administradores)
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    
    result = []
    for user in users:
        profile = crud.profile.get(db, id=user.profile_id)
        result.append({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "profile_name": profile.name if profile else None
        })
    
    return result


@router.put(
    "/users/{user_id}/deactivate",
    dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))]
)
def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Desactivar un usuario (solo administradores)
    """
    # No permitir desactivar al propio usuario
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta"
        )
    
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    crud.user.deactivate(db, id=user_id)
    return {"message": "Usuario desactivado exitosamente"}


@router.put(
    "/users/{user_id}/activate",
    dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))]
)
def activate_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Activar un usuario (solo administradores)
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    user.is_active = True
    crud.user.update(db, db_obj=user, obj_in={"is_active": True})
    return {"message": "Usuario activado exitosamente"}


@router.delete(
    "/users/{user_id}",
    dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))]
)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar un usuario permanentemente (solo administradores)
    """
    # No permitir eliminar al propio usuario
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    crud.user.delete(db, id=user_id)
    return {"message": "Usuario eliminado exitosamente"}
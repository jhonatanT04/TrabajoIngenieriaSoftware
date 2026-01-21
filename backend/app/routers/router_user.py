from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.db.database import get_session
from app.deps import *
from app.models.models import *
from app.crud.users_crud import *

from app.deps import get_db, DBSession
from app.auth.auth import RoleChecker, get_password_hash
from app.schemas import UserCreate, UserUpdate
router = APIRouter()


def format_user_response(user: User, db: DBSession):
    """Helper para formatear usuario con estructura esperada por Angular"""
    profile = None
    if user.profile_id:
        from app.crud.users_crud import profile as profile_crud
        profile = profile_crud.get(db, id=user.profile_id)
    
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "profile_id": str(user.profile_id),
        "profile": {
            "id": str(profile.id),
            "name": profile.name,
            "description": profile.description
        } if profile else None,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }


@router.post("/users", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_user(
    user_data: UserCreate,
    db: DBSession
):
    from app.crud.users_crud import user, profile
    from app.models.models import User as UserModel, Profile
    from app.auth.auth import get_password_hash
    
    existing = user.get_by_username(db, username=user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username ya existe")
    
    existing_email = user.get_by_email(db, email=user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email ya existe")
    
    profile_obj = profile.get_by_name(db, name=user_data.profile_name)
    if not profile_obj:
        profile_obj = Profile(name=user_data.profile_name)
        profile_obj = profile.create(db, obj_in=profile_obj)
    
    # Crear usuario directamente con el ORM
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        profile_id=profile_obj.id,
        is_active=user_data.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Retornar usuario con estructura esperada por Angular
    return {
        "id": str(new_user.id),
        "username": new_user.username,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "phone": new_user.phone,
        "profile_id": str(new_user.profile_id),
        "profile": {
            "id": str(profile_obj.id),
            "name": profile_obj.name,
            "description": profile_obj.description
        },
        "is_active": new_user.is_active,
        "created_at": new_user.created_at.isoformat(),
        "updated_at": new_user.updated_at.isoformat()
    }


@router.get("/users", tags=["Usuarios"])
async def list_users(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Numero de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros a retornar"),
    active_only: bool = Query(True, description="Filtrar solo usuarios activos")
):
    """
    Listar todos los usuarios (sin autenticación para desarrollo)
    
    Parametros de query:
    - skip: Paginacion - registros a saltar (default: 0)
    - limit: Cantidad maxima de registros (default: 100, max: 1000)
    - active_only: Mostrar solo activos (default: true)
    
    Retorna lista de usuarios con toda su informacion
    """
    from app.crud.users_crud import user
    
    if active_only:
        users = user.get_active_users(db)
    else:
        users = user.get_multi(db, skip=skip, limit=limit)
    
    # Formatear cada usuario con la estructura esperada por Angular
    return [format_user_response(u, db) for u in users]


@router.get("/users/{user_id}", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_user(
    user_id: UUID,
    db: DBSession
):
    """
    Obtener un usuario especifico por su ID
    
    Path params:
    - user_id: UUID del usuario
    
    Retorna el objeto usuario completo o 404 si no existe
    """
    from app.crud.users_crud import user
    
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return format_user_response(user_obj, db)


@router.get("/users/username/{username}", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_user_by_username(
    username: str,
    db: DBSession
):
    """
    Buscar usuario por nombre de usuario
    
    Path params:
    - username: Nombre de usuario a buscar
    
    Retorna el objeto usuario o 404 si no existe
    """
    from app.crud.users_crud import user
    
    user_obj = user.get_by_username(db, username=username)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return format_user_response(user_obj, db)


@router.put("/users/{user_id}", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: DBSession
):
    """
    Actualizar informacion de un usuario existente
    
    Path params:
    - user_id: UUID del usuario a actualizar
    
    Body: Permite actualizar datos básicos, rol y contraseña (opcional)
    
    Retorna el usuario actualizado o 404 si no existe
    """
    from app.crud.users_crud import user, profile
    from app.models.models import Profile
    from app.auth.auth import get_password_hash
    
    existing = user.get(db, id=user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = user_data.dict(exclude_unset=True)

    # Manejar cambio de contraseña si se envía
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Manejar cambio de rol por nombre de perfil
    if "profile_name" in update_data:
        profile_obj = profile.get_by_name(db, name=update_data["profile_name"])
        if not profile_obj:
            profile_obj = Profile(name=update_data["profile_name"])
            profile_obj = profile.create(db, obj_in=profile_obj)
        update_data["profile_id"] = profile_obj.id
        update_data.pop("profile_name", None)
    
    updated = user.update(db, db_obj=existing, obj_in=update_data)
    return format_user_response(updated, db)


@router.delete("/users/{user_id}/deactivate", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def deactivate_user(
    user_id: UUID,
    db: DBSession
):
    """
    Desactivar un usuario (soft delete)
    
    Path params:
    - user_id: UUID del usuario a desactivar
    
    No elimina el registro, solo cambia is_active a false
    Retorna el usuario desactivado
    """
    from app.crud.users_crud import user
    
    deactivated = user.deactivate(db, id=user_id)
    return format_user_response(deactivated, db)

@router.put("/users/{user_id}/activate",tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
def activate_user(
    user_id: UUID,
    db: Session = Depends(get_session)
):
    
    """
    Activar un usuario 
    
    Path params:
    - user_id: UUID del usuario a activar

    No elimina el registro, solo cambia is_active a true
    Retorna el usuario activado
    """
    from app.crud import users_crud

    user = users_crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    user.is_active = True
    users_crud.user.update(db, db_obj=user, obj_in={"is_active": True})
    actived = users_crud.user.get(db, id=user_id)
    return format_user_response(actived, db)


@router.get("/profiles", tags=["Perfiles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_profiles(db: DBSession):
    """
    Listar todos los perfiles/roles disponibles
    """
    from app.crud.users_crud import profile
    
    profiles = profile.get_multi(db)
    return profiles


@router.get("/profiles/{profile_id}", tags=["Perfiles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_profile(
    profile_id: UUID,
    db: DBSession
):
    """
    Obtener un perfil específico con sus permisos
    """
    from app.crud.users_crud import profile
    
    profile_obj = profile.get_with_permissions(db, id=profile_id)
    if not profile_obj:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile_obj


# ==================== ENDPOINTS DE ROLES (ALIAS PARA PROFILES) ====================
# Estos endpoints existen porque Angular espera /roles en lugar de /profiles

@router.get("/roles", tags=["Roles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_roles(db: DBSession):
    """
    Listar todos los roles disponibles
    Nota: Los roles son llamados "Profiles" en la base de datos
    """
    from app.crud.users_crud import profile
    
    roles = profile.get_multi(db)
    return roles


@router.get("/roles/{role_id}", tags=["Roles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def get_role(
    role_id: UUID,
    db: DBSession
):
    """
    Obtener un rol específico con sus permisos
    """
    from app.crud.users_crud import profile
    
    role_obj = profile.get_with_permissions(db, id=role_id)
    if not role_obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role_obj


@router.post("/roles", tags=["Roles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_role(
    role_data: dict = Body(...),
    db: DBSession = None
):
    """
    Crear un nuevo rol
    Body JSON esperado:
    {
        "name": "Nombre del Rol",
        "description": "Descripción del rol (opcional)"
    }
    """
    from app.crud.users_crud import profile
    from app.models.models import Profile
    
    # Validar que el nombre existe
    if not role_data.get("name"):
        raise HTTPException(status_code=400, detail="El nombre del rol es requerido")
    
    # Verificar que no existe un rol con ese nombre
    existing = profile.get_by_name(db, name=role_data.get("name"))
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")
    
    # Crear nuevo rol
    new_role = Profile(
        name=role_data.get("name"),
        description=role_data.get("description")
    )
    
    new_role = profile.create(db, obj_in=new_role)
    return new_role


@router.put("/roles/{role_id}", tags=["Roles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_role(
    role_id: UUID,
    role_data: dict = Body(...),
    db: DBSession = None
):
    """
    Actualizar un rol existente
    Body JSON esperado:
    {
        "name": "Nuevo nombre (opcional)",
        "description": "Nueva descripción (opcional)"
    }
    """
    from app.crud.users_crud import profile
    
    # Obtener rol existente
    existing_role = profile.get(db, id=role_id)
    if not existing_role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Actualizar
    updated_role = profile.update(db, db_obj=existing_role, obj_in=role_data)
    return updated_role


@router.delete("/roles/{role_id}", tags=["Roles"], dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def delete_role(
    role_id: UUID,
    db: DBSession
):
    """
    Eliminar un rol (solo si no tiene usuarios asignados)
    """
    from app.crud.users_crud import profile, user
    
    # Obtener rol
    role = profile.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Verificar si hay usuarios con este rol
    users_with_role = user.get_multi(db, filter_kwargs={"profile_id": role_id})
    if users_with_role and len(users_with_role) > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"No se puede eliminar el rol porque hay {len(users_with_role)} usuario(s) asignado(s)"
        )
    
    # Eliminar
    profile.delete(db, id=role_id)
    return {"message": "Rol eliminado exitosamente"}


@router.delete("/users/{user_id}",tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar un usuario permanentemente (solo administradores)
    """
    from app.crud import users_crud; 
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    user = users_crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    users_crud.user.delete(db, id=user_id)
    return {"message": "Usuario eliminado exitosamente"}
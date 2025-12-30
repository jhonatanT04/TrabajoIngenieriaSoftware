from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from db.database import get_session
from deps import *
from models.models import *
from crud.users_crud import *

from deps import get_db, DBSession
from auth.auth import RoleChecker
router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    profile_id: Optional[UUID] = None
    is_active: bool = True



@router.get("/users", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def list_users(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Numero de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros a retornar"),
    active_only: bool = Query(True, description="Filtrar solo usuarios activos")
):
    """
    Listar todos los usuarios
    
    Parametros de query:
    - skip: Paginacion - registros a saltar (default: 0)
    - limit: Cantidad maxima de registros (default: 100, max: 1000)
    - active_only: Mostrar solo activos (default: true)
    
    Retorna lista de usuarios con toda su informacion
    """
    from crud.users_crud import user
    
    if active_only:
        users = user.get_active_users(db)
    else:
        users = user.get_multi(db, skip=skip, limit=limit)
    
    return users


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
    from crud.users_crud import user
    
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_obj


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
    from crud.users_crud import user
    
    user_obj = user.get_by_username(db, username=username)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_obj


@router.put("/users/{user_id}", tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def update_user(
    user_id: UUID,
    user_data: UserCreate,
    db: DBSession
):
    """
    Actualizar informacion de un usuario existente
    
    Path params:
    - user_id: UUID del usuario a actualizar
    
    Body: Mismo formato que crear usuario
    
    Retorna el usuario actualizado o 404 si no existe
    """
    from crud.users_crud import user
    
    existing = user.get(db, id=user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    updated = user.update(db, db_obj=existing, obj_in=user_data.dict())
    return updated


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
    from crud.users_crud import user
    
    deactivated = user.deactivate(db, id=user_id)
    return {"message": "Usuario desactivado", "user": deactivated}

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
    from crud import users_crud

    user = users_crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    user.is_active = True
    users_crud.user.update(db, db_obj=user, obj_in={"is_active": True})
    actived = users_crud.user.get(db, id=user_id)
    return {"message": "Usuario activado", "user": actived}


@router.delete("/users/{user_id}",tags=["Usuarios"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar un usuario permanentemente (solo administradores)
    """
    from crud import users_crud; 
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
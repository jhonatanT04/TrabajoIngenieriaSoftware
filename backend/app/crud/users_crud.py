from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from app.models.models import (
    User, Profile, Permission, SystemParameter
)
from .base_crud import CRUDBase


class CRUDUser(CRUDBase[User, User, User]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        statement = select(User).where(User.username == username)
        return db.exec(statement).first()
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()
    
    def get_active_users(self, db: Session) -> List[User]:
        """Obtener todos los usuarios activos"""
        statement = select(User).where(User.is_active == True)
        return db.exec(statement).all()
    
    def get_by_profile(self, db: Session, *, profile_id: UUID) -> List[User]:
        """Obtener usuarios por perfil"""
        statement = select(User).where(User.profile_id == profile_id)
        return db.exec(statement).all()
    
    def update_password(self, db: Session, *, user: User, hashed_password: str) -> User:
        """Actualizar contraseña de usuario"""
        user.hashed_password = hashed_password
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def deactivate(self, db: Session, *, id: UUID) -> User:
        """Desactivar usuario"""
        user = self.get(db, id)
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


class CRUDProfile(CRUDBase[Profile, Profile, Profile]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Profile]:
        """Obtener perfil por nombre"""
        statement = select(Profile).where(Profile.name == name)
        return db.exec(statement).first()
    
    def get_with_permissions(self, db: Session, *, id: UUID) -> Optional[Profile]:
        """Obtener perfil con sus permisos"""
        profile = self.get(db, id)
        # SQLModel carga automáticamente las relaciones cuando se accede
        if profile:
            _ = profile.permissions  # Esto carga la relación
        return profile


class CRUDPermission(CRUDBase[Permission, Permission, Permission]):
    def get_by_module(self, db: Session, *, module_name: str) -> List[Permission]:
        """Obtener permisos por módulo"""
        statement = select(Permission).where(Permission.module_name == module_name)
        return db.exec(statement).all()
    
    def get_by_module_and_action(
        self, 
        db: Session, 
        *, 
        module_name: str, 
        action: str
    ) -> Optional[Permission]:
        """Obtener permiso específico"""
        statement = select(Permission).where(
            Permission.module_name == module_name,
            Permission.action == action
        )
        return db.exec(statement).first()


class CRUDSystemParameter(CRUDBase[SystemParameter, SystemParameter, SystemParameter]):
    def get_by_key(self, db: Session, *, key: str) -> Optional[SystemParameter]:
        """Obtener parámetro por clave"""
        statement = select(SystemParameter).where(SystemParameter.parameter_key == key)
        return db.exec(statement).first()
    
    def set_parameter(
        self, 
        db: Session, 
        *, 
        key: str, 
        value: str, 
        user_id: UUID
    ) -> SystemParameter:
        """Crear o actualizar parámetro"""
        param = self.get_by_key(db, key=key)
        if param:
            param.parameter_value = value
            param.updated_at = datetime.utcnow()
            param.updated_by = user_id
            db.add(param)
        else:
            param = SystemParameter(
                parameter_key=key,
                parameter_value=value,
                updated_by=user_id
            )
            db.add(param)
        db.commit()
        db.refresh(param)
        return param


# Instancias globales
user = CRUDUser(User)
profile = CRUDProfile(Profile)
permission = CRUDPermission(Permission)
system_parameter = CRUDSystemParameter(SystemParameter)
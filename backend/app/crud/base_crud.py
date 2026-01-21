from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlmodel import Session, select
from sqlmodel import SQLModel
from uuid import UUID

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD base con métodos por defecto para Create, Read, Update, Delete
        
        Args:
            model: Modelo SQLModel
        """
        self.model = model

    def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        """Obtener un registro por ID"""
        return db.get(self.model, id)

    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """Obtener múltiples registros con paginación"""
        statement = select(self.model).offset(skip).limit(limit)
        return db.exec(statement).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Crear un nuevo registro"""
        # Soporta tanto Pydantic (model_dump) como SQLModel (dict)
        if hasattr(obj_in, 'model_dump'):
            obj_in_data = obj_in.model_dump()
        elif hasattr(obj_in, 'dict'):
            obj_in_data = obj_in.dict()
        else:
            obj_in_data = dict(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """Actualizar un registro existente"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: UUID) -> ModelType:
        """Eliminar un registro"""
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        """Contar total de registros"""
        statement = select(self.model)
        return len(db.exec(statement).all())
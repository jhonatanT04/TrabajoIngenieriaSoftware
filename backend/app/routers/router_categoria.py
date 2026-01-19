from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import Optional
from uuid import UUID
from app.models.models import Category
from pydantic import BaseModel


from app.deps import  DBSession
from app.auth.auth import RoleChecker
router = APIRouter()

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[UUID] = None


@router.post("/categories", tags=["Categorias"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_category(
    category_data: CategoryCreate,
    db: DBSession
):
    """
    Crear nueva categoria de productos
    
    Campos requeridos:
    - name: Nombre de la categoria
    
    Campos opcionales:
    - description: Descripcion de la categoria
    - parent_category_id: UUID de categoria padre (para subcategorias)
    
    Ejemplo de Body JSON:
    ```json
    {
        "name": "Electronica",
        "description": "Productos electronicos"
    }
    ```
    """
    from crud.products_crud import category
    
    existing = category.get_by_name(db, name=category_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Categoria ya existe")
    
    new_category = Category(**category_data.dict())
    created = category.create(db, obj_in=new_category)
    
    return {
        "message": "Categoria creada exitosamente",
        "category": created
    }


@router.get("/categories", tags=["Categorias"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def list_categories(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros")
):
    """
    Listar todas las categorias
    
    Parametros de query:
    - skip: Paginacion (default: 0)
    - limit: Cantidad maxima (default: 100)
    
    Retorna lista completa de categorias
    """
    from crud.products_crud import category
    
    categories = category.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/categories/root", tags=["Categorias"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_root_categories(
    db: DBSession
):
    """
    Obtener categorias raiz (sin categoria padre)
    
    Retorna solo las categorias principales del primer nivel
    Util para construir menus jerarquicos
    """
    from crud.products_crud import category
    
    categories = category.get_root_categories(db)
    return categories


@router.get("/categories/{category_id}/subcategories", tags=["Categorias"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_subcategories(
    category_id: UUID,
    db: DBSession
):
    """
    Obtener subcategorias de una categoria
    
    Path params:
    - category_id: UUID de la categoria padre
    
    Retorna lista de categorias hijas
    Util para navegacion jerarquica
    """
    from crud.products_crud import category
    
    subcategories = category.get_subcategories(db, parent_id=category_id)
    return subcategories

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import Optional
from uuid import UUID
from app.models.models import Brand
from pydantic import BaseModel


from app.deps import  DBSession
from app.auth.auth import RoleChecker
router = APIRouter()

class BrandCreate(BaseModel):
    name: str
    description: Optional[str] = None
@router.post("/brands", tags=["Marcas"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador"]))])
async def create_brand(
    brand_data: BrandCreate,
    db: DBSession
):
    """
    Crear nueva marca de productos
    
    Campos requeridos:
    - name: Nombre de la marca
    
    Campos opcionales:
    - description: Descripcion de la marca
    
    Ejemplo de Body JSON:
    ```json
    {
        "name": "Samsung",
        "description": "Marca de electronicos"
    }
    ```
    """
    from app.crud.products_crud import brand
    
    existing = brand.get_by_name(db, name=brand_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Marca ya existe")
    
    new_brand = Brand(**brand_data.dict())
    created = brand.create(db, obj_in=new_brand)
    
    return {
        "message": "Marca creada exitosamente",
        "brand": created
    }


@router.get("/brands", tags=["Marcas"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def list_brands(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros")
):
    """
    Listar todas las marcas
    
    Parametros de query:
    - skip: Paginacion (default: 0)
    - limit: Cantidad maxima (default: 100)
    
    Retorna lista completa de marcas
    """
    from app.crud.products_crud import brand
    
    brands = brand.get_multi(db, skip=skip, limit=limit)
    return brands


@router.get("/brands/{brand_id}", tags=["Marcas"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_brand(
    brand_id: UUID,
    db: DBSession
):
    """
    Obtener marca especifica por ID
    
    Path params:
    - brand_id: UUID de la marca
    
    Retorna marca o 404
    """
    from app.crud.products_crud import brand
    
    brand_obj = brand.get(db, id=brand_id)
    if not brand_obj:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return brand_obj

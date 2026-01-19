from fastapi import APIRouter,Depends, HTTPException, Query, Body
from typing import  Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.models import Customer

from app.deps import get_db, DBSession
from app.auth.auth import RoleChecker
router = APIRouter()

class CustomerCreate(BaseModel):
    document_number: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True

@router.post("/customers", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def create_customer(
    customer_data: CustomerCreate,
    db: DBSession
):
    """
    Crear nuevo cliente
    
    Campos requeridos:
    - document_number: Cedula o RUC
    - first_name: Primer nombre
    - last_name: Apellido
    
    Campos opcionales:
    - email: Correo electronico
    - phone: Telefono
    - address: Direccion
    
    Ejemplo de Body JSON:
    ```json
    {
        "document_number": "0123456789",
        "first_name": "Juan",
        "last_name": "Perez",
        "email": "juan@example.com",
        "phone": "0999999999"
    }
    ```
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


@router.get("/customers", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def list_customers(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    active_only: bool = Query(True, description="Solo clientes activos")
):
    """
    Listar todos los clientes
    
    Parametros de query:
    - skip: Paginacion (default: 0)
    - limit: Cantidad maxima (default: 100)
    - active_only: Solo activos (default: true)
    
    Retorna lista de clientes
    """
    from crud.caja_crud import customer
    
    if active_only:
        customers = customer.get_active_customers(db)
        return customers[skip:skip+limit]
    else:
        return customer.get_multi(db, skip=skip, limit=limit)


@router.get("/customers/{customer_id}", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_customer(
    customer_id: UUID,
    db: DBSession
):
    """
    Obtener cliente especifico por ID
    
    Path params:
    - customer_id: UUID del cliente
    
    Retorna cliente o 404
    """
    from crud.caja_crud import customer
    
    cust = customer.get(db, id=customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cust


@router.get("/customers/document/{document_number}", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_customer_by_document(
    document_number: str,
    db: DBSession
):
    """
    Buscar cliente por numero de documento
    
    Path params:
    - document_number: Cedula o RUC del cliente
    
    Retorna cliente o 404
    """
    from crud.caja_crud import customer
    
    cust = customer.get_by_document(db, document_number=document_number)
    if not cust:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cust


@router.get("/customers/search/name", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def search_customers_by_name(
    db: DBSession,
    name: str = Query(..., min_length=2, description="Termino de busqueda")
):
    """
    Buscar clientes por nombre (busqueda parcial)
    
    Query params:
    - name: Termino de busqueda (minimo 2 caracteres)
    
    Busca en nombres y apellidos
    Retorna lista de clientes que coinciden
    """
    from crud.caja_crud import customer
    
    customers = customer.search_by_name(db, name=name)
    return customers


@router.get("/customers/vip/list", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_vip_customers(
    db: DBSession
):
    """
    Listar clientes VIP
    
    Retorna clientes marcados como VIP
    Util para promociones especiales
    """
    from crud.caja_crud import customer
    
    customers = customer.get_vip_customers(db)
    return customers


@router.get("/customers/top/list", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def get_top_customers(
    db: DBSession,
    limit: int = Query(10, ge=1, le=50, description="Cantidad de clientes top")
):
    """
    Top clientes por puntos de fidelidad
    
    Query params:
    - limit: Cantidad de clientes a retornar (default: 10, max: 50)
    
    Retorna clientes ordenados por puntos descendente
    Util para reportes y recompensas
    """
    from crud.caja_crud import customer
    
    customers = customer.get_top_customers(db, limit=limit)
    return customers


@router.post("/customers/{customer_id}/loyalty-points", tags=["Clientes"],dependencies=[Depends(RoleChecker(allowed_roles=["Administrador","Cajero"]))])
async def update_loyalty_points(
    customer_id: UUID,
    db: DBSession,
    points: float = Body(..., embed=True)
):
    """
    Actualizar puntos de fidelidad de un cliente
    
    Path params:
    - customer_id: UUID del cliente
    
    Body JSON:
    ```json
    {
        "points": 50.0
    }
    ```
    
    Suma los puntos al total existente
    Retorna cliente actualizado
    """
    from crud.caja_crud import customer
    
    updated = customer.update_loyalty_points(db, id=customer_id, points=points)
    return updated
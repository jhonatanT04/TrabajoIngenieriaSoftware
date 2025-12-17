from typing import Optional, List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(title="Backend FastAPI - Ejemplo")

# Modelos
class ItemBase(BaseModel):
    name: str = Field(..., example="Producto A")
    description: Optional[str] = Field(None, example="Descripción del producto")
    price: float = Field(0.0, ge=0, example=9.99)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)

class Item(ItemBase):
    id: UUID

# Almacenamiento en memoria (ejemplo)
_db: dict[UUID, Item] = {}

# Rutas
@app.get("/", tags=["salud"])
async def root():
    return {"status": "ok", "message": "Backend FastAPI funcionando"}

@app.post("/items/", response_model=Item, status_code=201, tags=["items"])
async def create_item(item: ItemCreate):
    item_id = uuid4()
    new_item = Item(id=item_id, **item.dict())
    _db[item_id] = new_item
    return new_item

@app.get("/items/", response_model=List[Item], tags=["items"])
async def list_items():
    return list(_db.values())

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def get_item(item_id: UUID):
    item = _db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: UUID, update: ItemUpdate):
    existing = _db.get(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    updated_data = existing.dict()
    update_fields = update.dict(exclude_unset=True)
    updated_data.update(update_fields)
    updated_item = Item(**updated_data)
    _db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def delete_item(item_id: UUID):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    del _db[item_id]
    return None

# Ejecutar con: python main.py  (o usar `uvicorn main:app --reload`)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
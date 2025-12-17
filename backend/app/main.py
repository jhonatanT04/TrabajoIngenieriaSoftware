from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from .database import init_db, get_session
from . import models, crud, auth, schemas, deps
from datetime import timedelta

app = FastAPI(title="Minimercado - Backend")

# CORS (allow frontend during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["salud"])
def root():
    return {"status": "ok", "message": "Backend Minimercado funcionando"}


@app.post("/auth/register", response_model=schemas.UserRead, tags=["auth"])
def register(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing = crud.get_user_by_username(session, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = auth.get_password_hash(user.password)
    new_user = crud.create_user(session, user.username, hashed, user.full_name or "", user.role)
    return new_user


@app.post("/auth/token", response_model=schemas.Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = crud.get_user_by_username(session, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    access_token = auth.create_access_token(str(user.id), expires_delta=timedelta(hours=12))
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/products/", response_model=schemas.ProductRead, tags=["products"])
def create_product(payload: schemas.ProductCreate, session: Session = Depends(get_session)):
    p = crud.create_product(session, **payload.dict())
    return p


@app.get("/products/", response_model=list[schemas.ProductRead], tags=["products"])
def list_products(session: Session = Depends(get_session)):
    return crud.list_products(session)


@app.post("/inventory/adjust", tags=["inventory"])
def adjust_stock(payload: schemas.InventoryMovementCreate, session: Session = Depends(get_session)):
    product = crud.adjust_stock(session, payload.product_id, payload.quantity, payload.reason)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"product_id": product.id, "stock": product.stock}


@app.post("/sales/", tags=["sales"])
def create_sale(payload: schemas.SaleCreate, session: Session = Depends(get_session)):
    # Simple sale implementation: validate products and decrement stock
    total = 0.0
    for item in payload.items:
        product = crud.get_product(session, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para producto {product.sku}")
        product.stock -= item.quantity
        total += item.quantity * item.price
        session.add(product)
    sale = models.Sale(customer_id=payload.customer_id, total=total)
    session.add(sale)
    session.commit()
    session.refresh(sale)
    return {"sale_id": sale.id, "total": sale.total}


@app.get("/users/me", response_model=schemas.UserRead, tags=["users"])
def read_current_user(current_user=Depends(deps.get_current_user)):
    return current_user

from sqlmodel import select
from sqlalchemy.exc import NoResultFound
from typing import Optional, List
from uuid import UUID
from models import models
from db.database import get_session

def get_user_by_username(session, username: str) -> Optional[models.User]:
    stmt = select(models.User).where(models.User.username == username)
    result = session.exec(stmt).first()
    return result

def get_user_by_id(session, user_id: str) -> Optional[models.User]:
    return session.get(models.User, user_id)

def create_user(session, username: str, hashed_password: str, full_name: str, role: str):
    user = models.User(username=username, hashed_password=hashed_password, full_name=full_name, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_product(session, **data) -> models.Product:
    p = models.Product(**data)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

def list_products(session) -> List[models.Product]:
    stmt = select(models.Product)
    return session.exec(stmt).all()

def get_product(session, product_id: UUID) -> Optional[models.Product]:
    return session.get(models.Product, product_id)

def adjust_stock(session, product_id: UUID, quantity: float, reason: str | None = None, user_id: UUID | None = None):
    product = get_product(session, product_id)
    if not product:
        return None
    product.stock += quantity
    movement = models.InventoryMovement(product_id=product_id, quantity=quantity, reason=reason, user_id=user_id)
    session.add(movement)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

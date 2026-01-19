#!/usr/bin/env python3
"""
Script para resetear la base de datos con datos iniciales
"""
import os
import sys
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlmodel import SQLModel, create_engine, Session
from uuid import uuid4
import logging

# Cargar variables de entorno
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar modelos
from app.models.models import Brand, CashRegister, Category, Customer, PaymentMethod, Product, Profile, User

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:123456e@localhost:5432/minimercado",
)

# Hash context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash una contraseña"""
    return pwd_context.hash(password)

def reset_database():
    """Reset database y crear datos iniciales"""
    engine = create_engine(DATABASE_URL, echo=False)
    
    # Drop all tables
    logger.info("Eliminando todas las tablas...")
    SQLModel.metadata.drop_all(engine)
    
    # Create all tables
    logger.info("Creando todas las tablas...")
    SQLModel.metadata.create_all(engine)
    
    # Seed data
    logger.info("Insertando datos iniciales...")
    with Session(engine) as session:
        # IDS FIJOS PARA RELACIONAR
        PROFILE_ADMIN_ID = uuid4()
        PROFILE_CASHIER_ID = uuid4()
        PROFILE_INVENTORY_ID = uuid4()
        PROFILE_MANAGER_ID = uuid4()
        PROFILE_SUPERVISOR_ID = uuid4()
        
        USER_ADMIN_ID = uuid4()
        
        # 1. PERFILES
        profiles = [
            Profile(id=PROFILE_ADMIN_ID, name="Administrador", description="Acceso total"),
            Profile(id=PROFILE_CASHIER_ID, name="Cajero", description="Solo ventas y caja"),
            Profile(id=PROFILE_INVENTORY_ID, name="Inventario", description="Gestión de stock"),
            Profile(id=PROFILE_MANAGER_ID, name="Gerente", description="Reportes y compras"),
            Profile(id=PROFILE_SUPERVISOR_ID, name="Supervisor", description="Anulaciones y cierres")
        ]
        session.add_all(profiles)
        session.commit()
        logger.info(f"✅ Insertados {len(profiles)} perfiles")
        
        # 2. USUARIOS
        admin_password_hash = hash_password("admin123")
        ana_password_hash = hash_password("ana123")
        carlos_password_hash = hash_password("carlos123")
        marta_password_hash = hash_password("marta123")
        
        logger.info(f"Admin hash: {admin_password_hash}")
        
        users = [
            User(id=USER_ADMIN_ID, username="admin", email="admin@minimercado.com", 
                 hashed_password=admin_password_hash, profile_id=PROFILE_ADMIN_ID, 
                 first_name="Justin", last_name="Admin", is_active=True),
            User(id=uuid4(), username="ana_caja", email="ana@mail.com", 
                 hashed_password=ana_password_hash, profile_id=PROFILE_CASHIER_ID, 
                 first_name="Ana", last_name="López", is_active=True),
            User(id=uuid4(), username="carlos_ventas", email="carlos@mail.com", 
                 hashed_password=carlos_password_hash, profile_id=PROFILE_CASHIER_ID, 
                 first_name="Carlos", last_name="Ruiz", is_active=True),
            User(id=uuid4(), username="marta_inv", email="marta@mail.com", 
                 hashed_password=marta_password_hash, profile_id=PROFILE_INVENTORY_ID, 
                 first_name="Marta", last_name="Sosa", is_active=True)
        ]
        session.add_all(users)
        session.commit()
        logger.info(f"✅ Insertados {len(users)} usuarios")
        logger.info("✅ Base de datos reseteada exitosamente")

if __name__ == "__main__":
    reset_database()

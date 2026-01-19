#!/usr/bin/env python3
"""
Script para actualizar hashes de usuarios en la base de datos
"""
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select
from uuid import uuid4
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:123456e@localhost:5432/minimercado",
)

# Importar modelos
from app.models.models import User

def update_user_hashes():
    """Actualizar hashes de usuarios"""
    engine = create_engine(DATABASE_URL, echo=False)
    
    # Hash bcrypt válido para: admin123
    ADMIN_HASH = "$2b$12$R26y18SexkGEkjvTqgagFOax11Uhw//EcpUZaOnrOXkgbgkaYLaFG"
    
    with Session(engine) as session:
        logger.info("Actualizando hashes de usuarios...")
        
        # Obtener todos los usuarios
        users = session.exec(select(User)).all()
        logger.info(f"Encontrados {len(users)} usuarios")
        
        # Actualizar hashes
        for user in users:
            logger.info(f"Actualizando usuario: {user.username}")
            user.hashed_password = ADMIN_HASH
        
        session.add_all(users)
        session.commit()
        
        logger.info("✅ Hashes actualizados exitosamente")

if __name__ == "__main__":
    update_user_hashes()

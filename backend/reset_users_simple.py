#!/usr/bin/env python3
"""
Script para resetear usuarios en la base de datos con contraseñas válidas
"""
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
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

def reset_users_only():
    """Reset solo los usuarios con contraseñas válidas"""
    engine = create_engine(DATABASE_URL, echo=False)
    
    # Hashes pre-calculados con bcrypt (de una contraseña test válida)
    # Estos hashes fueron generados con: bcrypt.hashpw(b'admin123', bcrypt.gensalt(rounds=12))
    # Pero como hay conflicto con bcrypt, usaremos un hash conocido válido
    
    with engine.begin() as conn:
        logger.info("Eliminando usuarios...")
        conn.exec_driver_sql("DELETE FROM \"user\" WHERE 1=1")
        conn.exec_driver_sql("DELETE FROM profile WHERE 1=1")
        
        logger.info("Insertando perfiles...")
        conn.exec_driver_sql("""
            INSERT INTO profile (id, name, description) VALUES 
              ('550e8400-e29b-41d4-a716-446655440001', 'Administrador', 'Acceso total'),
              ('550e8400-e29b-41d4-a716-446655440002', 'Cajero', 'Solo ventas y caja'),
              ('550e8400-e29b-41d4-a716-446655440003', 'Inventario', 'Gestión de stock')
        """)
        
        logger.info("Insertando usuarios...")
        # Hash válido para: admin123
        # Generado con: $2b$12$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK
        conn.exec_driver_sql("""
            INSERT INTO "user" (id, username, email, hashed_password, profile_id, first_name, last_name, is_active) VALUES 
              ('550e8400-e29b-41d4-a716-446655440004', 'admin', 'admin@minimercado.com', 
               '\\$2b\\$12\\$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', 
               '550e8400-e29b-41d4-a716-446655440001', 'Justin', 'Admin', true),
              ('550e8400-e29b-41d4-a716-446655440005', 'ana_caja', 'ana@mail.com', 
               '\\$2b\\$12\\$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', 
               '550e8400-e29b-41d4-a716-446655440002', 'Ana', 'López', true),
              ('550e8400-e29b-41d4-a716-446655440006', 'carlos_ventas', 'carlos@mail.com', 
               '\\$2b\\$12\\$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', 
               '550e8400-e29b-41d4-a716-446655440002', 'Carlos', 'Ruiz', true),
              ('550e8400-e29b-41d4-a716-446655440007', 'marta_inv', 'marta@mail.com', 
               '\\$2b\\$12\\$5i7UYlEzf/cSqfQ7RLNc0e/YXMX/GhGeHVVFQrfVRPLbxEJGqQjAK', 
               '550e8400-e29b-41d4-a716-446655440003', 'Marta', 'Sosa', true)
        """)
        
        logger.info("✅ Usuarios y perfiles reseteados exitosamente")

if __name__ == "__main__":
    reset_users_only()

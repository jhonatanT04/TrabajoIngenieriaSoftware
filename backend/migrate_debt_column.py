#!/usr/bin/env python3
"""
Script para hacer migración de la base de datos (agregar columna debt)
"""
import os
import sys
from sqlalchemy import text
from sqlmodel import create_engine, Session

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import DATABASE_URL

def main():
    """Ejecutar migración"""
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        try:
            # Verificar si la columna ya existe
            result = session.exec(
                text("SELECT column_name FROM information_schema.columns WHERE table_name='customers' AND column_name='debt'")
            ).first()
            
            if result:
                print("✅ La columna 'debt' ya existe en la tabla customers")
                return
            
            # Agregar la columna
            print("📝 Agregando columna 'debt' a la tabla customers...")
            session.exec(text("ALTER TABLE customers ADD COLUMN debt numeric NOT NULL DEFAULT 0.0"))
            session.commit()
            print("✅ Columna 'debt' agregada exitosamente")
            
        except Exception as e:
            print(f"❌ Error ejecutando migración: {e}")
            session.rollback()

if __name__ == "__main__":
    main()

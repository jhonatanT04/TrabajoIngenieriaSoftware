#!/usr/bin/env python3
"""
Script para limpiar la tabla de clientes
"""
import os
import sys
from sqlalchemy import text
from sqlmodel import create_engine, Session

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import DATABASE_URL

def main():
    """Limpiar tabla de clientes"""
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        try:
            print("🗑️  Limpiando datos relacionados...")
            # Eliminar en cascada (orden importante)
            session.exec(text("DELETE FROM sale_details"))
            session.exec(text("DELETE FROM sales"))
            session.exec(text("DELETE FROM invoices"))
            session.exec(text("DELETE FROM customer_preferences"))
            session.exec(text("DELETE FROM loyalty_transactions"))
            session.exec(text("DELETE FROM customer_notifications"))
            session.exec(text("DELETE FROM customers"))
            session.commit()
            print("✅ Tabla de clientes y datos relacionados limpiados")
        except Exception as e:
            print(f"❌ Error: {e}")
            session.rollback()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para llenar clientes de ejemplo en la base de datos
"""
import os
import sys
from datetime import datetime
from uuid import uuid4

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select, create_engine
from app.models.models import Customer
from app.db.database import DATABASE_URL

# Data de ejemplo
SAMPLE_CUSTOMERS = [
    {
        "document_type": "CEDULA",
        "document_number": "0991266692",
        "first_name": "Juan",
        "last_name": "Juan",
        "business_name": None,
        "email": "juan@gmail.com",
        "phone": "0991266692",
        "address": "Calle Principal 123",
        "city": "Quito",
        "preferred_contact_method": "EMAIL",
        "segment": "regular",
        "loyalty_points": 0.0,
        "debt": 0.0,
        "notes": "Cliente frecuente",
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0987654321",
        "first_name": "Hugo",
        "last_name": "Méndez",
        "business_name": None,
        "email": "hugo@gmail.com",
        "phone": "0987654321",
        "address": "Avenida Amazonas 456",
        "city": "Quito",
        "preferred_contact_method": "PHONE",
        "segment": "regular",
        "loyalty_points": 0.0,
        "debt": 0.0,
        "notes": None,
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "1234567890",
        "first_name": "Sofia",
        "last_name": "Vargas",
        "business_name": None,
        "email": "sofia@gmail.com",
        "phone": "0991234567",
        "address": "Calle 10 de Agosto 789",
        "city": "Cuenca",
        "preferred_contact_method": "EMAIL",
        "segment": "premium",
        "loyalty_points": 250.0,
        "debt": 0.0,
        "notes": "Cliente VIP",
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0909090909",
        "first_name": "Andrés",
        "last_name": "Castro",
        "business_name": None,
        "email": "andres@gmail.com",
        "phone": "0909090909",
        "address": "Pasaje 24 de Mayo 321",
        "city": "Guayaquil",
        "preferred_contact_method": "PHONE",
        "segment": "regular",
        "loyalty_points": 0.0,
        "debt": 0.0,
        "notes": None,
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0808080808",
        "first_name": "Paula",
        "last_name": "Navarro",
        "business_name": None,
        "email": "paula@gmail.com",
        "phone": "0808080808",
        "address": "Boulevard Naciones Unidas 654",
        "city": "Quito",
        "preferred_contact_method": "EMAIL",
        "segment": "regular",
        "loyalty_points": 0.0,
        "debt": 250.75,
        "notes": "Deuda pendiente",
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0707070707",
        "first_name": "Juan",
        "last_name": "Pérez",
        "business_name": None,
        "email": "juan@gmail.com",
        "phone": "0707070707",
        "address": "Calle Colón 987",
        "city": "Quito",
        "preferred_contact_method": "PHONE",
        "segment": "premium",
        "loyalty_points": 150.0,
        "debt": 0.0,
        "notes": "Cliente premium",
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0606060606",
        "first_name": "Maria",
        "last_name": "García",
        "business_name": None,
        "email": "maria@gmail.com",
        "phone": "0606060606",
        "address": "Avenida Patria 246",
        "city": "Quito",
        "preferred_contact_method": "EMAIL",
        "segment": "premium",
        "loyalty_points": 200.0,
        "debt": 0.0,
        "notes": "Cliente leal",
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0505050505",
        "first_name": "Pedro",
        "last_name": "Sánchez",
        "business_name": None,
        "email": "pedro@gmail.com",
        "phone": "0505050505",
        "address": "Calle García Moreno 135",
        "city": "Quito",
        "preferred_contact_method": "PHONE",
        "segment": "regular",
        "loyalty_points": 50.0,
        "debt": 0.0,
        "notes": None,
        "is_active": True,
    },
    {
        "document_type": "RUC",
        "document_number": "1710123456001",
        "first_name": "Empresa",
        "last_name": "ABC",
        "business_name": "ABC Distribuciones",
        "email": "info@abcdist.com",
        "phone": "0212342546",
        "address": "Polígono Industrial 999",
        "city": "Quito",
        "preferred_contact_method": "EMAIL",
        "segment": "premium",
        "loyalty_points": 500.0,
        "debt": 1500.00,
        "notes": "Empresa mayorista",
        "is_active": True,
    },
    {
        "document_type": "CEDULA",
        "document_number": "0404040404",
        "first_name": "Laura",
        "last_name": "López",
        "business_name": None,
        "email": "laura@gmail.com",
        "phone": "0404040404",
        "address": "Avenida Eloy Alfaro 555",
        "city": "Guayaquil",
        "preferred_contact_method": "EMAIL",
        "segment": "premium",
        "loyalty_points": 300.0,
        "debt": 0.0,
        "notes": "Cliente frecuente",
        "is_active": True,
    },
]

def main():
    """Crear y llenar tabla de clientes de ejemplo"""
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        # Verificar si ya existen clientes
        existing = session.exec(select(Customer)).first()
        if existing:
            print("⚠️  Ya hay clientes en la base de datos. Saltando inserción.")
            return
        
        print("📝 Insertando clientes de ejemplo...")
        
        for customer_data in SAMPLE_CUSTOMERS:
            customer = Customer(
                **customer_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(customer)
        
        session.commit()
        
        # Verificar inserción
        count = session.exec(select(Customer)).all()
        print(f"✅ {len(count)} clientes insertados exitosamente")

if __name__ == "__main__":
    main()

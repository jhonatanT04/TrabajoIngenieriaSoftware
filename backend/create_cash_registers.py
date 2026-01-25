"""
Script para crear cajas registradoras iniciales en la base de datos
Ejecutar: python create_cash_registers.py
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.append(str(Path(__file__).parent))

from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import CashRegister


def create_cash_registers():
    """Crear cajas registradoras iniciales si no existen"""
    
    cash_registers = [
        {
            "register_number": "Caja Principal",
            "location": "Piso 1 - Entrada",
            "is_active": True
        },
        {
            "register_number": "Caja 2",
            "location": "Piso 1 - Salida",
            "is_active": True
        },
        {
            "register_number": "Caja Express",
            "location": "Piso 2",
            "is_active": True
        }
    ]
    
    with Session(engine) as session:
        created_count = 0
        
        for register_data in cash_registers:
            # Verificar si ya existe
            existing = session.exec(
                select(CashRegister).where(
                    CashRegister.register_number == register_data["register_number"]
                )
            ).first()
            
            if not existing:
                cash_register = CashRegister(**register_data)
                session.add(cash_register)
                created_count += 1
                print(f"✓ Creada: {register_data['register_number']} - {register_data['location']}")
            else:
                print(f"○ Ya existe: {register_data['register_number']}")
        
        session.commit()
        
        # Mostrar todas las cajas
        print("\n" + "="*60)
        print("CAJAS REGISTRADORAS EN EL SISTEMA:")
        print("="*60)
        
        all_registers = session.exec(
            select(CashRegister).order_by(CashRegister.register_number)
        ).all()
        
        for register in all_registers:
            status = "✓ Activa" if register.is_active else "✗ Inactiva"
            print(f"{register.register_number:20} | {register.location or 'Sin ubicación':25} | {status}")
        
        print("="*60)
        print(f"\nTotal de cajas: {len(all_registers)}")
        print(f"Cajas creadas en esta ejecución: {created_count}")


if __name__ == "__main__":
    try:
        print("Iniciando creación de cajas registradoras...")
        print("-" * 60)
        create_cash_registers()
        print("\n✓ Proceso completado exitosamente")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)

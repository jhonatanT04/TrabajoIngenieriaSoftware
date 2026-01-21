"""
Script para resetear e inicializar la base de datos con datos de prueba
"""
import sys
sys.path.append('.')

from app.db.database import init_db, seed_data, engine
from sqlmodel import SQLModel

def reset_database():
    """Elimina y recrea todas las tablas"""
    print("🗑️  Eliminando tablas existentes...")
    SQLModel.metadata.drop_all(engine)
    print("✅ Tablas eliminadas")
    
    print("\n📦 Creando tablas...")
    init_db()
    print("✅ Tablas creadas")
    
    print("\n🌱 Insertando datos iniciales...")
    seed_data()
    print("✅ Datos insertados")
    
    print("\n✅ Base de datos lista!")
    print("\n👤 Usuario de prueba:")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    try:
        reset_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

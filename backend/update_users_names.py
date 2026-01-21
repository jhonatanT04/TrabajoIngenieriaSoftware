#!/usr/bin/env python3
"""
Script para actualizar nombres de usuarios de ejemplo
"""
import sys
sys.path.insert(0, '/c/Users/mlata/Desktop/TrabajoIngenieriaSoftware/backend')

from sqlmodel import Session, select
from app.db.database import engine
from app.models.models import User

def update_user_names():
    with Session(engine) as session:
        # Obtener todos los usuarios
        users = session.exec(select(User)).all()
        
        print(f"Encontrados {len(users)} usuarios")
        print("=" * 60)
        
        updated = 0
        for user in users:
            print(f"\nUsuario: {user.username}")
            print(f"  ID: {user.id}")
            print(f"  First Name: {user.first_name}")
            print(f"  Last Name: {user.last_name}")
            
            # Actualizar si no tienen nombres
            if not user.first_name or not user.last_name:
                # Generar nombre basado en el username
                first_name = user.username.split('_')[0].capitalize() if '_' in user.username else user.username.capitalize()
                last_name = 'Vendedor'
                
                user.first_name = first_name
                user.last_name = last_name
                
                print(f"  ✅ Actualizando a: {first_name} {last_name}")
                session.add(user)
                updated += 1
        
        if updated > 0:
            session.commit()
            print(f"\n{'=' * 60}")
            print(f"✅ {updated} usuarios actualizados exitosamente")
        else:
            print(f"\n{'=' * 60}")
            print(f"✅ Todos los usuarios ya tienen nombres configurados")

if __name__ == "__main__":
    try:
        update_user_names()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

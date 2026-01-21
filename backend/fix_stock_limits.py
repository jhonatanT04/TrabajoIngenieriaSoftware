"""
Script para ajustar los valores de stock_min y stock_max de manera coherente
con el stock actual de cada producto
"""
from sqlmodel import Session, select
from app.models.models import Product, Inventory
from app.db.database import engine

def fix_stock_limits():
    with Session(engine) as session:
        # Obtener todos los productos
        products = session.exec(select(Product)).all()
        
        print(f"Ajustando límites de stock para {len(products)} productos...\n")
        
        for product in products:
            # Obtener inventario del producto
            inventory = session.exec(
                select(Inventory).where(Inventory.product_id == product.id)
            ).first()
            
            current_stock = inventory.quantity if inventory else 0
            
            # Calcular valores coherentes basados en el stock actual
            if current_stock == 0:
                # Si no hay stock, establecer límites bajos
                stock_min = 5
                stock_max = 50
            else:
                # stock_min = 20% del stock actual (mínimo 5)
                stock_min = max(5, int(current_stock * 0.2))
                # stock_max = 200% del stock actual (mínimo stock_min + 20)
                stock_max = max(stock_min + 20, int(current_stock * 2))
            
            # Actualizar producto
            old_min = product.stock_min
            old_max = product.stock_max
            
            product.stock_min = stock_min
            product.stock_max = stock_max
            
            session.add(product)
            
            print(f"✓ {product.name} ({product.sku})")
            print(f"  Stock actual: {current_stock}")
            print(f"  Antes: min={old_min}, max={old_max}")
            print(f"  Ahora: min={stock_min}, max={stock_max}")
            print()
        
        session.commit()
        print("✅ Límites de stock ajustados correctamente!")

if __name__ == "__main__":
    fix_stock_limits()

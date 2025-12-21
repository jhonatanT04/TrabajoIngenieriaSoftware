import os
from models.models import Brand, CashRegister, Category, Customer, PaymentMethod, Product, Profile, User
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from dotenv import load_dotenv
from uuid import uuid4
import logging

# Cargar variables de entorno desde .env
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:root@localhost:5432/minimercado",
)

engine = create_engine(DATABASE_URL, echo=False)
logger = logging.getLogger("app.database")


def init_db() -> None:
    """Create database tables."""
    try:
        # Crear todas las tablas
        SQLModel.metadata.create_all(engine)
        
        tables = sorted(SQLModel.metadata.tables.keys())
        logger.info(f"✅ Base de datos inicializada con {len(tables)} tablas")
        logger.info(f"Tablas creadas: {', '.join(tables)}")
        
    except Exception as exc:
        print(f"\n❌ ERROR ORIGINAL DE POSTGRES: {exc}\n")
        raise RuntimeError(
            "No se pudo inicializar la base de datos. Verifique DATABASE_URL y que Postgres esté en ejecución. " + DATABASE_URL
        ) from exc


def seed_data() -> None:
    """Insertar datos iniciales en la base de datos."""
    try:
        with Session(engine) as session:
            # Verificar si ya hay datos
            if session.query(Profile).first():
                logger.info("⚠️  La base de datos ya contiene datos. Saltando seed.")
                return
            
            logger.info("🌱 Insertando datos iniciales...")
            
            # IDS FIJOS PARA RELACIONAR
            PROFILE_ADMIN_ID = uuid4()
            PROFILE_CASHIER_ID = uuid4()
            PROFILE_INVENTORY_ID = uuid4()
            PROFILE_MANAGER_ID = uuid4()
            PROFILE_SUPERVISOR_ID = uuid4()
            
            USER_ADMIN_ID = uuid4()
            CAT_ABARROTES_ID = uuid4()
            CAT_BEBIDAS_ID = uuid4()
            CAT_LIMPIEZA_ID = uuid4()
            CAT_LACTEOS_ID = uuid4()
            CAT_CARNES_ID = uuid4()
            CAT_SNACKS_ID = uuid4()
            CAT_PANADERIA_ID = uuid4()
            CAT_HIGIENE_ID = uuid4()
            CAT_MASCOTAS_ID = uuid4()
            CAT_FRUTAS_ID = uuid4()
            
            BRAND_NESTLE_ID = uuid4()
            BRAND_COCACOLA_ID = uuid4()
            
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
            users = [
                User(id=USER_ADMIN_ID, username="admin", email="admin@minimercado.com", 
                     hashed_password="pbkdf2:sha256:600000$placeholder", profile_id=PROFILE_ADMIN_ID, 
                     first_name="Justin", last_name="Admin"),
                User(id=uuid4(), username="ana_caja", email="ana@mail.com", 
                     hashed_password="pbkdf2:sha256:600000$placeholder", profile_id=PROFILE_CASHIER_ID, 
                     first_name="Ana", last_name="López"),
                User(id=uuid4(), username="carlos_ventas", email="carlos@mail.com", 
                     hashed_password="pbkdf2:sha256:600000$placeholder", profile_id=PROFILE_CASHIER_ID, 
                     first_name="Carlos", last_name="Ruiz"),
                User(id=uuid4(), username="marta_inv", email="marta@mail.com", 
                     hashed_password="pbkdf2:sha256:600000$placeholder", profile_id=PROFILE_INVENTORY_ID, 
                     first_name="Marta", last_name="Sosa")
            ]
            session.add_all(users)
            session.commit()
            logger.info(f"✅ Insertados {len(users)} usuarios")
            
            # 3. CATEGORÍAS
            categories = [
                Category(id=CAT_ABARROTES_ID, name="Abarrotes", description="Productos básicos"),
                Category(id=CAT_BEBIDAS_ID, name="Bebidas", description="Refrescos y aguas"),
                Category(id=CAT_LIMPIEZA_ID, name="Limpieza", description="Hogar"),
                Category(id=CAT_LACTEOS_ID, name="Lácteos", description="Leche y derivados"),
                Category(id=CAT_CARNES_ID, name="Carnes", description="Cortes de res y pollo"),
                Category(id=CAT_SNACKS_ID, name="Snacks", description="Frituras y dulces"),
                Category(id=CAT_PANADERIA_ID, name="Panadería", description="Pan fresco"),
                Category(id=CAT_HIGIENE_ID, name="Higiene", description="Cuidado personal"),
                Category(id=CAT_MASCOTAS_ID, name="Mascotas", description="Comida perros/gatos"),
                Category(id=CAT_FRUTAS_ID, name="Frutas y Verduras", description="Orgánicos")
            ]
            session.add_all(categories)
            session.commit()
            logger.info(f"✅ Insertadas {len(categories)} categorías")
            
            # 4. MARCAS
            brands = [
                Brand(id=BRAND_NESTLE_ID, name="Nestlé"),
                Brand(id=BRAND_COCACOLA_ID, name="Coca-Cola"),
                Brand(id=uuid4(), name="P&G"),
                Brand(id=uuid4(), name="Unilever"),
                Brand(id=uuid4(), name="Colgate"),
                Brand(id=uuid4(), name="Gloria"),
                Brand(id=uuid4(), name="PepsiCo"),
                Brand(id=uuid4(), name="Kellogg's"),
                Brand(id=uuid4(), name="Bimbo"),
                Brand(id=uuid4(), name="Kraft")
            ]
            session.add_all(brands)
            session.commit()
            logger.info(f"✅ Insertadas {len(brands)} marcas")
            
            # 5. PRODUCTOS
            products = [
                Product(sku="PROD-001", barcode="775001", name="Arroz Extra 1kg", 
                       category_id=CAT_ABARROTES_ID, cost_price=0.80, sale_price=1.20, stock_min=20),
                Product(sku="PROD-002", barcode="775002", name="Aceite Girasol 1L", 
                       category_id=CAT_ABARROTES_ID, cost_price=1.50, sale_price=2.10, stock_min=10),
                Product(sku="PROD-003", barcode="775003", name="Coca Cola 3L", 
                       category_id=CAT_BEBIDAS_ID, cost_price=1.80, sale_price=2.50, stock_min=15),
                Product(sku="PROD-004", barcode="775004", name="Leche Entera 1L", 
                       category_id=CAT_LACTEOS_ID, cost_price=0.60, sale_price=0.95, stock_min=30),
                Product(sku="PROD-005", barcode="775005", name="Detergente 500g", 
                       category_id=CAT_LIMPIEZA_ID, cost_price=1.10, sale_price=1.60, stock_min=10),
                Product(sku="PROD-006", barcode="775006", name="Papel Higiénico 4u", 
                       category_id=CAT_HIGIENE_ID, cost_price=0.90, sale_price=1.40, stock_min=20),
                Product(sku="PROD-007", barcode="775007", name="Atún en Conserva", 
                       category_id=CAT_ABARROTES_ID, cost_price=0.75, sale_price=1.30, stock_min=50),
                Product(sku="PROD-008", barcode="775008", name="Yogurt Fresa 1L", 
                       category_id=CAT_LACTEOS_ID, cost_price=1.20, sale_price=1.85, stock_min=12),
                Product(sku="PROD-009", barcode="775009", name="Pan de Molde", 
                       category_id=CAT_PANADERIA_ID, cost_price=1.40, sale_price=2.00, stock_min=15),
                Product(sku="PROD-010", barcode="775010", name="Agua Mineral 600ml", 
                       category_id=CAT_BEBIDAS_ID, cost_price=0.25, sale_price=0.50, stock_min=100)
            ]
            session.add_all(products)
            session.commit()
            logger.info(f"✅ Insertados {len(products)} productos")
            
            # 6. CLIENTES
            customers = [
                Customer(document_number="12345678", first_name="Juan", last_name="Pérez", 
                        email="juan@gmail.com", loyalty_points=150),
                Customer(document_number="87654321", first_name="Maria", last_name="García", 
                        email="maria@gmail.com", loyalty_points=200),
                Customer(document_number="11223344", first_name="Pedro", last_name="Sánchez", 
                        email="pedro@gmail.com"),
                Customer(document_number="55667788", first_name="Lucía", last_name="Fernández"),
                Customer(document_number="99001122", first_name="Marcos", last_name="Torres"),
                Customer(document_number="33445566", first_name="Elena", last_name="Ríos"),
                Customer(document_number="77889900", first_name="Hugo", last_name="Méndez"),
                Customer(document_number="22334455", first_name="Sofia", last_name="Vargas"),
                Customer(document_number="44556677", first_name="Andrés", last_name="Castro"),
                Customer(document_number="66778899", first_name="Paula", last_name="Navarro")
            ]
            session.add_all(customers)
            session.commit()
            logger.info(f"✅ Insertados {len(customers)} clientes")
            
            # 7. CAJAS
            registers = [
                CashRegister(register_number="CAJA-01", location="Puerta Principal"),
                CashRegister(register_number="CAJA-02", location="Pasillo Central"),
                CashRegister(register_number="CAJA-03", location="Segundo Piso")
            ]
            session.add_all(registers)
            session.commit()
            logger.info(f"✅ Insertadas {len(registers)} cajas registradoras")
            
            # 8. MÉTODOS DE PAGO
            payment_methods = [
                PaymentMethod(name="Efectivo"),
                PaymentMethod(name="Tarjeta de Crédito"),
                PaymentMethod(name="Transferencia"),
                PaymentMethod(name="Yape / Plin")
            ]
            session.add_all(payment_methods)
            session.commit()
            logger.info(f"✅ Insertados {len(payment_methods)} métodos de pago")
            
            logger.info("🎉 Datos iniciales insertados correctamente")
            
    except Exception as exc:
        logger.error(f"❌ Error al insertar datos iniciales: {exc}")
        raise


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
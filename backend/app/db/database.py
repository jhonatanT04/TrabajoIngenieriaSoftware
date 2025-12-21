import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:root@localhost:5432/minimercado",
)

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Create database tables."""
    try:
        # IMPORTANTE: Importar todos los modelos antes de crear las tablas
         # noqa: F401
        
        # Crear todas las tablas
        SQLModel.metadata.create_all(engine)
        
        import logging
        logger = logging.getLogger("app.database")
        tables = sorted(SQLModel.metadata.tables.keys())
        logger.info(f"✅ Base de datos inicializada con {len(tables)} tablas")
        logger.info(f"Tablas creadas: {', '.join(tables)}")
        SQLModel.metadata.create_all(engine)
        
    except Exception as exc:
        print(f"\n❌ ERROR ORIGINAL DE POSTGRES: {exc}\n")
        raise RuntimeError(
            "No se pudo inicializar la base de datos. Verifique DATABASE_URL y que Postgres esté en ejecución. "+ DATABASE_URL
        ) from exc


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
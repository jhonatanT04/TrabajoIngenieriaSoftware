import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Use DATABASE_URL env var if set. Default to the user's PostgreSQL settings.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://minimercado:1234@localhost:5432/minimercado_db",
)

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Create database tables. If the DB is unreachable, raise an informative error."""
    try:
        # Import models so SQLModel metadata is populated (necessary for create_all to see tables)
        try:
            import app.models as _models  # noqa: F401
        except Exception:
            # If models cannot be imported, still attempt create_all (useful in some test setups)
            pass

        SQLModel.metadata.create_all(engine)
        # Log which tables exist in metadata (helpful for debugging)
        try:
            import logging

            logger = logging.getLogger("app.database")
            tables = sorted(SQLModel.metadata.tables.keys())
            logger.info("Tablas disponibles en metadata: %s", tables)
        except Exception:
            pass
    except Exception as exc:
        # Provide a clear error message to help with configuration
        raise RuntimeError(
            "No se pudo inicializar la base de datos. Verifique DATABASE_URL y que Postgres esté en ejecución."
        ) from exc


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

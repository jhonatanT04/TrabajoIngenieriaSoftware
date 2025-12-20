"""Helper script to create tables in the database configured by DATABASE_URL.
Run: python scripts/create_tables.py
"""
import os
from backend.app.db.database import init_db

if __name__ == "__main__":
    print("Using DATABASE_URL:", os.environ.get("DATABASE_URL"))
    print("Creating tables...")
    init_db()
    print("Done.")

"""Database connection and initialization helper module."""
import sqlite3
from pathlib import Path
from flask import g, current_app

def get_db(db_path=None):
    """Get a database connection for the current application context or path."""
    if db_path is not None:
        conn = sqlite3.connect(str(db_path), timeout=60.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    if "db" not in g:
        path = current_app.config["DATABASE_PATH"]
        conn = sqlite3.connect(str(path), timeout=60.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        g.db = conn
    return g.db

def close_db(e=None):
    """Close the database connection if open."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(db_path=None):
    """Initialize database schema from database/schema.sql."""
    schema_path = Path(__file__).resolve().parent / "database" / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_db(db_path)
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        if db_path is not None:
            conn.close()

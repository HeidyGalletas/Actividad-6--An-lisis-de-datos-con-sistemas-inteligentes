"""Módulo de base de datos para el servidor MCP de inventario."""

from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = str(BASE_DIR / "inventory.db")


def init_db() -> None:
    """Crea la base de datos SQLite y la tabla productos si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            precio REAL NOT NULL CHECK(precio >= 0)
        )
        """
    )

    conn.commit()
    conn.close()


def reset_db() -> None:
    """Limpia la tabla productos. Se usa solo para pruebas funcionales."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'productos'")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Base de datos inicializada en: {DB_NAME}")

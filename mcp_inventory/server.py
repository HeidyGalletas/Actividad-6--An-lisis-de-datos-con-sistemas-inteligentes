"""Servidor MCP para gestionar un inventario con SQLite.

Actividad 6 - Computación Cognitiva para Big Data
Tema: Desarrollo de un sistema cognitivo usando MCP y bases de datos.
"""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List

from database import DB_NAME, init_db

# Compatibilidad con variantes de la librería FastMCP.
try:
    from mcp.server.fastmcp import FastMCP  # type: ignore
except ImportError:  # pragma: no cover
    try:
        from fastmcp import FastMCP  # type: ignore
    except ImportError:  # pragma: no cover
        class FastMCP:  # type: ignore
            """Fallback mínimo para permitir pruebas locales sin fastmcp instalado."""

            def __init__(self, name: str) -> None:
                self.name = name

            def tool(self):
                def decorator(func):
                    return func
                return decorator

            def run(self) -> None:
                raise RuntimeError("Instale la librería fastmcp para ejecutar el servidor MCP.")

            def serve(self) -> None:
                self.run()


init_db()
mcp = FastMCP("InventarioDB")


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión a SQLite con filas consultables por nombre."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convierte una fila SQLite en un diccionario estándar."""
    return {
        "id": row["id"],
        "nombre": row["nombre"],
        "categoria": row["categoria"],
        "cantidad": row["cantidad"],
        "precio": row["precio"],
    }


def validar_producto(nombre: str, cantidad: int, precio: float) -> None:
    """Valida datos básicos antes de insertar o actualizar productos."""
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del producto es obligatorio.")
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa.")
    if precio < 0:
        raise ValueError("El precio no puede ser negativo.")


@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float) -> str:
    """Crea un producto en el inventario."""
    validar_producto(nombre, cantidad, precio)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
        (nombre.strip(), categoria.strip(), cantidad, precio),
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return f"Producto creado exitosamente con id {nuevo_id}."


@mcp.tool()
def consultar_producto(id: int) -> Dict[str, Any]:
    """Consulta un producto por su identificador."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row_to_dict(row)
    return {"error": "Producto no encontrado."}


@mcp.tool()
def actualizar_producto(id: int, cantidad: int) -> str:
    """Actualiza la cantidad disponible de un producto."""
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa.")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id))
    conn.commit()
    filas = cursor.rowcount
    conn.close()

    if filas == 0:
        return "No se actualizó ningún registro porque el producto no existe."
    return "Producto actualizado correctamente."


@mcp.tool()
def eliminar_producto(id: int) -> str:
    """Elimina un producto por su identificador."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    filas = cursor.rowcount
    conn.close()

    if filas == 0:
        return "No se eliminó ningún registro porque el producto no existe."
    return "Producto eliminado correctamente."


@mcp.tool()
def listar_productos() -> List[Dict[str, Any]]:
    """Lista todos los productos registrados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    return [row_to_dict(row) for row in rows]


@mcp.tool()
def calcular_valor_total_inventario() -> Dict[str, float]:
    """Calcula el valor total del inventario: suma de cantidad * precio."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(cantidad * precio) AS total FROM productos")
    total = cursor.fetchone()["total"]
    conn.close()

    return {"valor_total_inventario": float(total or 0)}


@mcp.tool()
def productos_agotados() -> List[Dict[str, Any]]:
    """Retorna los productos cuya cantidad es igual a cero."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad = 0 ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    return [row_to_dict(row) for row in rows]


@mcp.tool()
def producto_mas_costoso() -> Dict[str, Any]:
    """Identifica el producto con mayor precio unitario."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY precio DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return row_to_dict(row)
    return {"error": "No hay productos registrados."}


@mcp.tool()
def estadisticas_inventario() -> Dict[str, float]:
    """Calcula estadísticas generales del inventario."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_productos,
            AVG(cantidad) AS promedio_cantidad,
            AVG(precio) AS promedio_precio,
            SUM(cantidad * precio) AS valor_total
        FROM productos
        """
    )
    row = cursor.fetchone()
    conn.close()

    return {
        "total_productos": int(row["total_productos"] or 0),
        "promedio_cantidad": float(row["promedio_cantidad"] or 0),
        "promedio_precio": float(row["promedio_precio"] or 0),
        "valor_total": float(row["valor_total"] or 0),
    }


if __name__ == "__main__":
    # En algunas versiones se usa run() y en otras serve().
    if hasattr(mcp, "run"):
        mcp.run()
    else:
        mcp.serve()

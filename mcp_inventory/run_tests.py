"""Pruebas funcionales básicas para el servidor MCP de inventario.

Este archivo ejecuta las funciones directamente para validar la lógica del taller.
"""

from pprint import pprint

from database import reset_db
from server import (
    actualizar_producto,
    calcular_valor_total_inventario,
    consultar_producto,
    crear_producto,
    eliminar_producto,
    estadisticas_inventario,
    listar_productos,
    producto_mas_costoso,
    productos_agotados,
)


def main() -> None:
    reset_db()

    print("1. Crear mínimo cinco productos")
    productos = [
        ("Laptop Lenovo ThinkPad", "Tecnología", 5, 2500000),
        ("Mouse inalámbrico", "Accesorios", 10, 45000),
        ("Teclado mecánico", "Accesorios", 8, 180000),
        ("Monitor 24 pulgadas", "Tecnología", 3, 850000),
        ("Cable HDMI", "Cables", 0, 30000),
    ]
    for producto in productos:
        print(crear_producto(*producto))

    print("\n2. Consultar un producto por identificador")
    pprint(consultar_producto(1))

    print("\n3. Actualizar la cantidad de un producto")
    print(actualizar_producto(2, 25))
    pprint(consultar_producto(2))

    print("\n4. Eliminar un producto")
    print(eliminar_producto(3))

    print("\n5. Listar todos los productos registrados")
    pprint(listar_productos())

    print("\n6. Calcular el valor total del inventario")
    pprint(calcular_valor_total_inventario())

    print("\n7. Consultar productos agotados")
    pprint(productos_agotados())

    print("\n8. Identificar el producto más costoso")
    pprint(producto_mas_costoso())

    print("\n9. Consultar estadísticas generales del inventario")
    pprint(estadisticas_inventario())


if __name__ == "__main__":
    main()

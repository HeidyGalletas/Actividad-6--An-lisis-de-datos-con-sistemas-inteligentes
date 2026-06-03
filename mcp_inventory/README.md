# Servidor MCP de Inventario con SQLite

Proyecto académico para la actividad **Desarrollo de un Sistema Cognitivo usando MCP y Bases de Datos**. El sistema implementa un servidor MCP en Python que permite gestionar productos de inventario mediante operaciones CRUD y consultas analíticas básicas.

## 1. Requisitos

- Python 3.8 o superior
- SQLite3
- Visual Studio Code o editor similar
- Git y GitHub
- Librería `fastmcp`

## 2. Estructura del proyecto

```text
mcp_inventory/
├── database.py
├── server.py
├── run_tests.py
├── requirements.txt
├── README.md
└── inventory.db  # se genera automáticamente al ejecutar el proyecto
```

## 3. Instalación

Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 4. Inicialización de la base de datos

```bash
python database.py
```

El comando crea el archivo `inventory.db` y la tabla `productos` con los campos `id`, `nombre`, `categoria`, `cantidad` y `precio`.

## 5. Ejecución del servidor MCP

```bash
python server.py
```

El servidor expone herramientas para crear, consultar, actualizar, eliminar y listar productos, además de calcular estadísticas de inventario.

## 6. Pruebas funcionales

Para ejecutar una prueba completa de las funciones principales:

```bash
python run_tests.py
```

Las pruebas realizan las siguientes acciones:

1. Crear cinco productos.
2. Consultar un producto por identificador.
3. Actualizar la cantidad de un producto.
4. Eliminar un producto.
5. Listar todos los productos registrados.
6. Calcular el valor total del inventario.
7. Consultar productos agotados.
8. Identificar el producto más costoso.
9. Consultar estadísticas generales del inventario.

## 7. Herramientas implementadas

| Herramienta | Descripción |
|---|---|
| `crear_producto` | Registra un producto con nombre, categoría, cantidad y precio. |
| `consultar_producto` | Busca un producto por su identificador. |
| `actualizar_producto` | Actualiza la cantidad disponible de un producto. |
| `eliminar_producto` | Elimina un producto del inventario. |
| `listar_productos` | Lista todos los productos registrados. |
| `calcular_valor_total_inventario` | Calcula la suma de cantidad por precio de todos los productos. |
| `productos_agotados` | Retorna los productos con cantidad igual a cero. |
| `producto_mas_costoso` | Identifica el producto con mayor precio unitario. |
| `estadisticas_inventario` | Calcula total de productos, promedios y valor total. |


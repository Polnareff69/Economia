import psycopg2
import random
from datetime import datetime, timedelta

# Conectar con la base de datos PostgreSQL (reemplaza con tus credenciales)
conn = psycopg2.connect(
    dbname="Modelos Economicos",  # Nombre de tu base de datos
    user="Polnareff",                # Tu usuario de PostgreSQL
    password="26910531camila",         # Tu contraseña de PostgreSQL
    host="LocalHost",                 # Dirección del servidor (usualmente localhost)
    port="5432"                       # Puerto por defecto de PostgreSQL
)
cursor = conn.cursor()

# Crear la tabla en PostgreSQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id SERIAL PRIMARY KEY,
        fecha_venta DATE,
        nombre_producto TEXT,
        precio DECIMAL(7, 0),
        cantidad_ventas INT
    )
''')

# Función para generar una venta aleatoria
def generar_venta(fecha):
    productos = ["Producto A", "Producto B", "Producto C", "Producto D"]
    nombre_producto = random.choice(productos)
    precio = round(random.uniform(45000, 65000), 2)  # Precio entre 10 y 100
    cantidad_ventas = random.randint(1, 100)  # Entre 1 y 100 ventas
    return (fecha, nombre_producto, precio, cantidad_ventas)

# Generar 4 años de datos (1460 días)
start_date = datetime(2021, 2, 9)
end_date = start_date + timedelta(days=1460)

fecha_actual = start_date
while fecha_actual <= end_date:
    venta = generar_venta(fecha_actual.strftime('%Y-%m-%d'))
    cursor.execute('''
        INSERT INTO ventas (fecha_venta, nombre_producto, precio, cantidad_ventas)
        VALUES (%s, %s, %s, %s)
    ''', venta)
    fecha_actual += timedelta(days=1)

# Confirmar y cerrar la conexión
conn.commit()
cursor.close()
conn.close()
print("Datos insertados correctamente.")

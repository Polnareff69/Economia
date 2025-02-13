import random
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
cur = conn.cursor()

# Obtener todos los registros y actualizar 'cantidad_ofrecida'
cur.execute("SELECT id, cantidad_ofrecida FROM ventas")
registros = cur.fetchall()

# Iterar sobre cada registro y actualizar la columna 'cantidad_ofrecida'
for registro in registros:
    id_registro = registro[0]
    cantidad_ofrecida = registro[1]
    
    # Generar un número aleatorio entre 20 y 100
    incremento = random.randint(20, 100)
    nueva_cantidad = incremento

    # Actualizar el registro con la nueva cantidad_ofrecida
    cur.execute("""
        UPDATE ventas
        SET cantidad_ofrecida = %s
        WHERE id = %s
    """, (nueva_cantidad, id_registro))

# Confirmar los cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()

print("Datos actualizados correctamente.")
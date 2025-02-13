import psycopg2
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Conexión a la base de datos (ajusta los parámetros según tu configuración)
conn = psycopg2.connect(
    dbname="Modelos Economicos",  # Nombre de tu base de datos
    user="Polnareff",                # Tu usuario de PostgreSQL
    password="26910531camila",         # Tu contraseña de PostgreSQL
    host="LocalHost",                 # Dirección del servidor (usualmente localhost)
    port="5432"                       # Puerto por defecto de PostgreSQL
)
cursor = conn.cursor()

# Obtener los datos de ventas
query = '''
    SELECT fecha_venta, nombre_producto, precio, cantidad_ventas, cantidad_ofrecida
    FROM ventas
'''
cursor.execute(query)

# Cargar los datos en un DataFrame de pandas
ventas_df = pd.DataFrame(cursor.fetchall(), columns=['fecha_venta', 'nombre_producto', 'precio', 'cantidad_ventas', 'cantidad_ofrecida'])

# Cerrar la conexión
cursor.close()
conn.close()

# Ver los primeros registros
print(ventas_df.head())


# Agrupar las ventas por producto y calcular la cantidad total vendida y el precio promedio
ventas_agrupadas = ventas_df.groupby(['nombre_producto', 'fecha_venta']).agg(
    cantidad_total=('cantidad_ventas', 'sum'),
    precio_promedio=('precio', 'mean')
).reset_index()

# Ver los datos agrupados
print(ventas_agrupadas.head())

ventas_agrupadasOferta = ventas_df.groupby(['nombre_producto', 'fecha_venta']).agg(
    cantidad_totalOfrecida=('cantidad_ofrecida', 'sum'),
    precio_promedio=('precio', 'mean')
).reset_index()

print(ventas_agrupadasOferta.head())



# Seleccionar las columnas relevantes
Y = pd.to_numeric(ventas_agrupadas['precio_promedio'])  # Precio
X = pd.to_numeric(ventas_agrupadas['cantidad_total'])  # Cantidad total demandada


# Añadir una constante a X (intercepto de la regresión)
X = sm.add_constant(X)

# Realizar la regresión lineal
modelo_d = sm.OLS(Y, X).fit()

# Ver los resultados de la regresión (los parámetros estimados)
print(modelo_d.summary())


y_oferta = pd.to_numeric(ventas_agrupadasOferta['precio_promedio'])  # Precio
X_oferta = pd.to_numeric(ventas_agrupadasOferta['cantidad_totalOfrecida'])  # Cantidad ofrecida

# Añadir una constante a X
X_oferta = sm.add_constant(X_oferta)

# Realizar la regresión
modelo_s = sm.OLS(y_oferta, X_oferta).fit()

# Ver los resultados de la regresión (los parámetros estimados)
print(modelo_s.summary())




# Graficar la curva de demanda
plt.figure(figsize=(10, 6))
plt.scatter(ventas_agrupadas['cantidad_total'], ventas_agrupadas['precio_promedio'],color='blue', label='Datos de Demanda')
plt.plot(ventas_agrupadas['cantidad_total'], modelo_d.predict(X), color='red', label='Curva de Demanda', linewidth=2)

# Graficar la curva de oferta (si tienes los datos de oferta)
plt.scatter(ventas_agrupadasOferta['cantidad_totalOfrecida'], ventas_agrupadasOferta['precio_promedio'], color='green', label='Datos de Oferta')
plt.plot(ventas_agrupadasOferta['cantidad_totalOfrecida'], modelo_s.predict(X_oferta), color='orange', label='Curva de Oferta', linewidth=2)

plt.xlabel('Cantidad')
plt.ylabel('Precio')
plt.title('Curvas de Oferta y Demanda')
plt.legend()
plt.show()

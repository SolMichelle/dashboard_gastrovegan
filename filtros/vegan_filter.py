import pandas as pd
from esquema.restaurante import Restaurante

# Lectura del archivo colocado en la carpeta data

df_original = pd.read_csv("data/vegetarian_vegan_restaurants.csv")

# Simular el filtro para quedarse con los registros marcadamente Veganos o Plant-Based
# Filtrar filas donde la descripción o el nombre contenga la palabra "vegan"
df_veganas = df_original[df_original['categories'].str.contains('Vegan', case=False, na=False)].copy()

# Estandarizar los nombres de las columnas usando nuestro esquema
df_veganas = df_veganas.rename(columns={
    "name": Restaurante.COL_NOMBRE,
    "city": Restaurante.COL_CIUDAD,
    "menus.amountMax": Restaurante.COL_PRECIO
})

df_veganas = df_veganas[[Restaurante.COL_NOMBRE, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO]]

df_veganas[Restaurante.COL_TIPO] = "Vegano"
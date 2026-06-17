import pandas as pd
from esquema.restaurante import Restaurante

# Leemos la misma fuente de datos de restaurantes
df_original = pd.read_csv("data/vegetarian_vegan_restaurants.csv")

# Filtramos los registros que son Vegetarianos pero no estrictamente Veganos para separar los conjuntos
df_vegetarianas = df_original[
    df_original['categories'].str.contains('Vegetarian', case=False, na=False) & 
    ~df_original['categories'].str.contains('Pure Vegan', case=False, na=False)
].copy()

# Estandarizamos las columnas con la misma estructura de la clase Restaurante
df_vegetarianas = df_vegetarianas.rename(columns={
    "name": Restaurante.COL_NOMBRE,
    "city": Restaurante.COL_CIUDAD,
    "menus.amountMax": Restaurante.COL_PRECIO
})

# Seleccionamos las columnas del esquema
df_vegetarianas = df_vegetarianas[[Restaurante.COL_NOMBRE, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO]]

# Asignamos la etiqueta de tipo correspondiente
df_vegetarianas[Restaurante.COL_TIPO] = "Vegetariano"
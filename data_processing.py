import pandas as pd
# Importamos los DataFrames filtrados desde la carpeta filters
from esquema.restaurante import Restaurante
from filtros.vegan_filter import df_veganas
from filtros.vegetarian_filter import df_vegetarianas

print("Iniciando el procesamiento y unificación de datos gastronómicos...")

# Concatenamos los dos DataFrames (Veganos y Vegetarianos) usando una unión interna (inner)
# tal como en tu modelo de clase
df_establecimientos = pd.concat([df_veganas, df_vegetarianas], join="inner", ignore_index=True)

# Opcional: Eliminar duplicados si un restaurante comparte ambas categorías
df_final_mercado = df_establecimientos.drop_duplicates(subset=['nombre_local', 'ciudad']).reset_index(drop=True)

# tasa de cambio
TASA_CAMBIO_ARS = 1455.0

# nueva columna multiplicando la columna original en USD
df_final_mercado[Restaurante.COL_PRECIO_ARS] = df_final_mercado[Restaurante.COL_PRECIO] * TASA_CAMBIO_ARS

# redondeo a 2 decimales 
df_final_mercado[Restaurante.COL_PRECIO_ARS] = df_final_mercado[Restaurante.COL_PRECIO_ARS].round(2)

print(f"Procesamiento completado con éxito. Total de registros unificados: {len(df_final_mercado)}")

# Este dataframe unificado quedará disponible para que lo consuma el esquema o la vista
# data_processing.py
import pandas as pd
# Importamos los DataFrames filtrados desde la carpeta filters
from filtros.vegan_filter import df_veganas
from filtros.vegetarian_filter import df_vegetarianas

print("Iniciando el procesamiento y unificación de datos gastronómicos...")

# Concatenamos los dos DataFrames (Veganos y Vegetarianos) usando una unión interna (inner)
# tal como en tu modelo de clase
df_establecimientos = pd.concat([df_veganas, df_vegetarianas], join="inner", ignore_index=True)

# Opcional: Eliminar duplicados si un restaurante comparte ambas categorías
df_final_mercado = df_establecimientos.drop_duplicates(subset=['nombre_local', 'ciudad']).reset_index(drop=True)

print(f"Procesamiento completado con éxito. Total de registros unificados: {len(df_final_mercado)}")

# Este dataframe unificado quedará disponible para que lo consuma el esquema o la vista
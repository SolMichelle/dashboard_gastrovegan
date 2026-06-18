import pandas as pd
import json
# Importamos los DataFrames filtrados 
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

# Cargamos el archivo JSON estructurado con la densidad y poder adquisitivo local
with open("data/mercado_argentino.json", "r", encoding="utf-8") as f:
    datos_argentina = json.load(f)

# Bucle de negocio: calcula el score de oportunidad dinámicamente con Pandas
for zona in datos_argentina:
    # Multiplicamos Densidad * Poder Adquisitivo como indicador proxy de éxito comercial
    score_crudo = (zona["poblacion_densidad_km2"] * zona["poder_adquisitivo_promedio_ars"]) / 1_000_000
    zona["score_inversion"] = round(score_crudo, 2)

print("Integración de la fuente sociodemográfica argentina completada.")

with open("data/mercado_argentino.json", "r", encoding="utf-8") as f:
    datos_json_arg = json.load(f)

# Convertimos el JSON a DataFrame de Pandas para que la vista lo pueda importar sin errores
df_argentina = pd.DataFrame(datos_json_arg)

# Operación vectorial con Pandas: calculamos el score directo en las columnas
df_argentina["score_inversion"] = (df_argentina["poblacion_densidad_km2"] * df_argentina["poder_adquisitivo_promedio_ars"]) / 1_000_000
df_argentina["score_inversion"] = df_argentina["score_inversion"].round(2)

print("Integración de la fuente sociodemográfica argentina completada en formato Pandas.")

#PROCESAMIENTO CON PANDAS DEL JSON DE PLATOS "VEGANIZABLES"
df_platos = pd.read_json("data/platos_argentinos.json")
# Limpieza rápida: ordenamos por costo de menor a mayor
df_platos = df_platos.sort_values(by="costo_insumos_ars").reset_index(drop=True)

print("Procesamiento completado. Todas las fuentes se convirtieron a estructuras Pandas.")
import pandas as pd
from esquema.restaurante import Restaurante

# 1. Carga del dataset oficial de datos.gob.ar
df_gob = pd.read_csv("densidad.csv") # Este archivo se descartó por mala calidad de datos, pero se deja el código para mostrar el proceso de integración de fuentes

# 2. Renombrado y limpieza según lo visto en clase
df_gob = df_gob.rename(columns={
    "provincia_nombre": Restaurante.COL_PROVINCIA,
    "poblacion_densidad": Restaurante.COL_DENSIDAD 
})

# 3. Agregar la variable proxy de nivel adquisitivo (NBS) simulada por provincia
# Basado en datos macro del INDEC
mapa_adquisitivo = {
    "Ciudad Autónoma de Buenos Aires": 92.5,
    "Mendoza": 84.0,
    "Córdoba": 85.5,
    "Santa Fe": 83.2,
    "Provincia de Buenos Aires": 78.0
}

df_gob[Restaurante.COL_NIVEL_ADQUISITIVO] = df_gob[Restaurante.COL_PROVINCIA].map(mapa_adquisitivo).fillna(70.0)

df_argentina = df_gob[[Restaurante.COL_PROVINCIA, Restaurante.COL_DENSIDAD, Restaurante.COL_NIVEL_ADQUISITIVO]].copy()
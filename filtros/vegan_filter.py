import pandas as pd
from esquema.restaurante import Restaurante

# Leemos el archivo original de restaurantes de Datafiniti (Kaggle) colocado en la carpeta data
# Nota: Si usas formato CSV usamos read_csv, si el profesor exige read_xml o similar por el ejercicio de clase, se puede adaptar.
df_original = pd.read_csv("data/vegetarian_vegan_restaurants.csv")

# Simulamos el filtro para quedarnos con los registros marcadamente Veganos o Plant-Based
# Filtramos filas donde la descripción o el nombre contenga la palabra "vegan"
df_veganas = df_original[df_original['categories'].str.contains('Vegan', case=False, na=False)].copy()

# Estandarizamos los nombres de las columnas usando nuestro esquema, tal como en tu modelo
df_veganas = df_veganas.rename(columns={
    "name": Restaurante.COL_NOMBRE,
    "city": Restaurante.COL_CIUDAD,
    "menus.amountMax": Restaurante.COL_PRECIO
})

# Nos quedamos únicamente con las columnas que le interesan a nuestro negocio
df_veganas = df_veganas[[Restaurante.COL_NOMBRE, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO]]

# Asignamos la etiqueta fija de tipo, igual que df_hongos["tipo"] = "Hongo"
df_veganas[Restaurante.COL_TIPO] = "Vegano"
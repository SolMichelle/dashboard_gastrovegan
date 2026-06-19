import pandas as pd
from esquema.restaurante import Restaurante


df_original = pd.read_csv("data/vegetarian_vegan_restaurants.csv")


df_vegetarianas = df_original[
    df_original['categories'].str.contains('Vegetarian', case=False, na=False) & 
    ~df_original['categories'].str.contains('Pure Vegan', case=False, na=False)
].copy()


df_vegetarianas = df_vegetarianas.rename(columns={
    "name": Restaurante.COL_NOMBRE,
    "city": Restaurante.COL_CIUDAD,
    "menus.amountMax": Restaurante.COL_PRECIO
})


df_vegetarianas = df_vegetarianas[[Restaurante.COL_NOMBRE, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO]]


df_vegetarianas[Restaurante.COL_TIPO] = "Vegetariano"
class Restaurante:
    # Constantes de clase para estandarizar las columnas del DataFrame final
    COL_NOMBRE = "nombre_local"
    COL_CIUDAD = "ciudad"
    COL_PRECIO = "precio_plato"
    COL_PRECIO_ARS = "precio_ars"  
    COL_TIPO = "tipo_oferta"  # "Vegano" o "Vegetariano"
    COL_PROVINCIA = "provincia"
    COL_DENSIDAD = "densidad_poblacion"  # habitantes por km² (del CSV de datos.gob.ar)
    COL_NIVEL_ADQUISITIVO = "indice_nbs" # población con NBS (%)
    COL_SCORE_INVERSION = "score_oportunidad" # métrica calculada con Pandas

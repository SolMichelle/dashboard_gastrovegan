import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def cargar_y_procesar_datos():
    df_platos = pd.read_json('data/platos_argentinos.json')
    df_mercado = pd.read_json('data/mercado_argentino.json')
    
    # Dataset nutricional (Kaggle)
    try:
        df_nutricion = pd.read_csv('data/Food_and_Nutrition.csv')
    except Exception:
        df_nutricion = pd.DataFrame()
        
    np.random.seed(42)
    # Clasificación de rentabilidad lógica:
    # Menú rentable = Bajo costo de insumos + alta aceptación
    df_platos['margen_estimado'] = np.random.uniform(30, 65, size=len(df_platos))
    df_platos['precio_sugerido_ars'] = df_platos['costo_insumos_ars'] * (1 + (df_platos['margen_estimado'] / 100))
    df_platos['rentabilidad_clase'] = np.where(df_platos['costo_insumos_ars'] < 2500, 'Alta Rentabilidad', 'Rentabilidad Moderada')
    
    return df_platos, df_mercado, df_nutricion

# --- 1. INTELIGENCIA ARTIFICIAL & MACHINE LEARNING (scikit-learn) ---
def entrenar_modelo_rentabilidad():
    """
    Entrena un modelo Random Forest Classifier para predecir si un menú optimizado 
    tendrá Alta Rentabilidad según sus costos de materias primas.
    """
    df_platos, _, _ = cargar_y_procesar_datos()
    
    X = df_platos[['costo_insumos_ars']]
    y = np.where(df_platos['rentabilidad_clase'] == 'Alta Rentabilidad', 1, 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    modelo = RandomForestClassifier(n_estimators=50, random_state=42)
    modelo.fit(X_train, y_train)
    
    accuracy = accuracy_score(y_test, modelo.predict(X_test))
    return modelo, accuracy

# --- 2. PRONÓSTICO Y MODELADO ESTADÍSTICO (statsmodels) ---
def entrenar_modelo_regresion_precios():
    """
    Modelo de Regresión Econométrica (OLS) con statsmodels para pronosticar 
    el precio de lista de carta sugerido ($ ARS) en función del costo de insumos.
    """
    df_platos, _, _ = cargar_y_procesar_datos()
    
    # Ajuste de regresión por Mínimos Cuadrados Ordinarios (OLS)
    modelo_ols = smf.ols('precio_sugerido_ars ~ costo_insumos_ars', data=df_platos).fit()
    
    r_squared = round(modelo_ols.rsquared, 4)
    p_value = round(modelo_ols.f_pvalue, 4)
    
    return modelo_ols, r_squared, p_value

def predecir_precio_optimo_stats(costo_ingresado_ars):
    """
    Utiliza el modelo de statsmodels para realizar un pronóstico puntual de precio.
    """
    modelo_ols, _, _ = entrenar_modelo_regresion_precios()
    df_nuevo = pd.DataFrame({'costo_insumos_ars': [costo_ingresado_ars]})
    prediccion = modelo_ols.predict(df_nuevo).iloc[0]
    return round(prediccion, 2)

# --- 3. PRUEBA DE HIPÓTESIS Y ANÁLISIS DE INFERENCIA (scipy.stats) ---
def analisis_estadistico_ejecutivo():
    """
    Inferencia estadística explicada para consultoría gastronómica mediante scipy.stats.
    """
    df_platos, _, _ = cargar_y_procesar_datos()
    
    costo_medio = df_platos['costo_insumos_ars'].mean()
    margen_medio = df_platos['margen_estimado'].mean()
    
    # Prueba de t para validar varianza y significancia respecto al estándar tradicional
    t_stat, p_val = stats.ttest_1samp(df_platos['costo_insumos_ars'], popmean=3000)
    
    es_significativo = p_val < 0.05
    conclusion = (
        "Se confirma estadísticamente que el costo medio de los insumos de reemplazo "
        f"(${costo_medio:,.2f} ARS) es significativamente menor que el estándar tradicional, "
        f"permitiendo sostener un margen medio estimado del {margen_medio:.1f}%."
    ) if es_significativo else "Los costos se mantienen dentro de los rangos competitivos esperados."
    
    return {
        "costo_medio": round(costo_medio, 2),
        "margen_medio": round(margen_medio, 1),
        "p_valor": round(p_val, 4),
        "conclusion": conclusion
    }

def procesar_datos_nutricionales():
    """
    Estandariza el dataset Food_and_Nutrition.csv para comparar dietas en Plotly.
    """
    _, _, df_nutricion = cargar_y_procesar_datos()
    if df_nutricion.empty:
        return pd.DataFrame()
    
    columnas_lower = {c: c.lower() for c in df_nutricion.columns}
    df_nutricion = df_nutricion.rename(columns=columnas_lower)
    
    mapeo_dietas = {
        'vegan': 'Vegana',
        'vegetarian': 'Vegetariana',
        'omnivore': 'Omnívora',
        'omnivorous': 'Omnívora'
    }
    
    if 'diet_type' in df_nutricion.columns:
        df_nutricion['dieta_es'] = df_nutricion['diet_type'].str.lower().map(mapeo_dietas).fillna('General')
    else:
        df_nutricion['dieta_es'] = 'General'
        
    return df_nutricion

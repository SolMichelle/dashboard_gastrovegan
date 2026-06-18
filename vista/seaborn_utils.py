import matplotlib.pyplot as plt
import base64, io, seaborn

def dispersion(df, series, x, y, limites=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Renderizado híbrido scatter + lmplot
    seaborn.scatterplot(data=df, x=x, y=y, hue=series, ax=ax)
    
    plt.title("Línea de Tendencia y Dispersión de Costos ($ ARS)")
    plt.ylabel("Precio en $ ARS")
    plt.xlabel("Índice de Registros de Muestra")
    
    if limites:
        plt.ylim(bottom=limites.get("bottom", None), top=limites.get("top", None))
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    seaborn_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return seaborn_img
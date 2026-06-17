import matplotlib.pyplot as plt
import base64, io, seaborn

def dispersion(df, series: str, x: str, y: str, limites: dict[str,float] = {"bottom": 0, "left": 0}):
    plt.figure()
    
    # Si la variable X o Y del dataset original no son puramente continuas, creamos un índice para mapear la dispersión
    # o usamos el precio mapeado directamente.
    seaborn.scatterplot(df, x=x, y=y, hue=series)
    seaborn.lmplot(df, x=x, y=y, hue=series)
    
    plt.xlim(left=limites.get("left", None), right=limites.get("right", None))
    plt.ylim(bottom=limites.get("bottom", None), top=limites.get("top", None))
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    seaborn_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return seaborn_img
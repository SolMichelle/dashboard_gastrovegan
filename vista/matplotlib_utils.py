import matplotlib.pyplot as plt
import io, base64

def cajas_y_bigotes(dataframe, columna_mostrada: str, columna_agrupadora: str):
    plt.figure()
    valores_agrupadores = sorted(set(dataframe[columna_agrupadora]))
    
    plt.boxplot(
        [
            dataframe[dataframe[columna_agrupadora] == valor][columna_mostrada]
            for valor in valores_agrupadores
        ],
        patch_artist=True,  # Rellenar las cajas
        showfliers=False,   # Quitar moscas/outliers
    )
    
    plt.title(f"Distribución de {columna_mostrada.replace('_', ' ')}s en Matplotlib")
    # Ponemos las etiquetas de forma dinámica según los tipos del dataset (Vegano / Vegetariano)
    plt.xticks(range(1, len(valores_agrupadores) + 1), valores_agrupadores)
    plt.ylabel("Valores ($)")
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    matplotlib_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return matplotlib_img
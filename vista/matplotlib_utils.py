import matplotlib.pyplot as plt
import io, base64

def cajas_y_bigotes(dataframe, columna_mostrada, columna_agrupadora):
    plt.figure(figsize=(6, 4))
    valores_agrupadores = sorted(set(dataframe[columna_agrupadora]))
    
    plt.boxplot(
        [
            dataframe[dataframe[columna_agrupadora] == valor][columna_mostrada]
            for valor in valores_agrupadores
        ],
        patch_artist=True,
        showfliers=False
    )
    plt.title("Distribución de Precios Competitivos en Pesos ($ ARS)")
    plt.xticks(range(1, len(valores_agrupadores) + 1), valores_agrupadores)
    plt.ylabel("Precio en $ ARS")
    plt.grid(True, linestyle="--", alpha=0.6)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    matplotlib_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return matplotlib_img

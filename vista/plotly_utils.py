import plotly.express as px
import plotly.io as pio

pio.renderers.default = "iframe"

def grafico_barras(df, x: str, y: str):
    # Agrupamos por la variable X (ej: ciudad) y promediamos el valor del precio (Y)
    df_agrupado = df[[x, y]].groupby(x)[y].mean().reset_index()
    
    return px.bar(
        df_agrupado,
        x=y,
        y=x,
        orientation="h",
        title=f"Promedio de {y.replace('_', ' ')}s por {x.replace('_', ' ')}".capitalize(),
        color_discrete_sequence=['#1b4d3e'] # Verde culinario/sustentable
    )

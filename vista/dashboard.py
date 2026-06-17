from dash import Dash, html, dcc
from data_processing import df_final_mercado  # Importamos el dataframe unificado
from esquema.restaurante import Restaurante    # Columnas estandarizadas
from vista.matplotlib_utils import cajas_y_bigotes
from vista.seaborn_utils import dispersion
from vista.plotly_utils import grafico_barras

app = Dash(__name__)

IMG_BASE64 = "data:image/png;base64,{}"

# Para que Seaborn tenga una variable numérica X contra la cual graficar el precio,
# creamos temporalmente una columna de índice de posición en el layout.
df_render = df_final_mercado.copy()
df_render['indice_registro'] = range(len(df_render))

app.layout = html.Div(
    [
        html.H1("Plataforma Analítica de Inteligencia Gastronómica Plant-Based", style={'color': '#1b4d3e', 'textAlign': 'center'}),
        html.P("Herramienta interactiva y estática para la toma de decisiones en consultoría de menús veganos.", style={'textAlign': 'center'}),
        
        html.H2("Análisis Estático de Precios (Matplotlib)"),
        html.P("Muestra la dispersión de precios y los rangos de mercado de la oferta vegana vs vegetariana:"),
        html.Img(
            src=IMG_BASE64.format(
                cajas_y_bigotes(df_render, Restaurante.COL_PRECIO, Restaurante.COL_TIPO)
            )
        ),
        
        html.H2("Tendencia y Regresión de Costos (Seaborn)"),
        html.P("Líneas de tendencia de precios máximos detectados en los registros procesados:"),
        html.Div(
            [
                html.Img(
                    src=IMG_BASE64.format(
                        dispersion(
                            df_render,
                            Restaurante.COL_TIPO,
                            'indice_registro',
                            Restaurante.COL_PRECIO,
                        )
                    )
                ),
                html.Img(
                    src=IMG_BASE64.format(
                        dispersion(
                            df_render,
                            Restaurante.COL_TIPO,
                            'indice_registro',
                            Restaurante.COL_PRECIO,
                            {"bottom": 0, "left": 0, "right": len(df_render), "top": df_render[Restaurante.COL_PRECIO].max() + 5}
                        )
                    )
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
        
        html.H2("Análisis Comparativo por Ciudades (Plotly Interactivo)"),
        html.P("Explore de forma interactiva el comportamiento de precios promedio según la región geográfica:"),
        dcc.Graph(
            figure=grafico_barras(df_render, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO),
            style={"height": "60vh"}
        ),
    ]
)

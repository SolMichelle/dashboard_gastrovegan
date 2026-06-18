from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from data_processing import df_final_mercado
from esquema.restaurante import Restaurante
from vista.matplotlib_utils import cajas_y_bigotes
from vista.seaborn_utils import dispersion
from vista.plotly_utils import grafico_barras

# Inicio usando el tema MINTY 
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

IMG_BASE64 = "data:image/png;base64,{}"

df_render = df_final_mercado.copy()
df_render['indice_registro'] = range(len(df_render))

# CONTENEDOR PRINCIPAL CON LA GUÍA DE ESTILO
app.layout = dbc.Container(fluid=True, style={"backgroundColor": "#fcfcfc", "padding": "30px"}, children=[
    
    # ENCABEZADO PRINCIPAL (Introducción al problema)
    dbc.Row(className="mb-5", children=[
        dbc.Col(style={"textAlign": "center"}, children=[
            html.H1("Plataforma de Inteligencia Gastronómica Plant-Based", 
                    style={"color": "#1b4d3e", "fontWeight": "bold", "fontSize": "28pt"}),
            html.H5("Análisis de Oportunidades de Negocio y Mitigación del 'Comensal Veto' mediante Ciencia de Datos", 
                    style={"color": "#618274", "fontStyle": "italic"}),
            html.Hr(style={"borderColor": "#8fbc8f", "borderWidth": "2px", "width": "60%", "margin": "auto"})
        ])
    ]),

    # SECCIÓN 1: KPIs MACRO (justificación del mercado con fuentes teóricas)
    dbc.Row(className="mb-4 text-center", children=[
        dbc.Col(md=4, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3("12.4%", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Crecimiento Anual Mercado Vegano (Grand View Research)", style={"color": "#7f8c8d", "fontSize": "9.5pt"})
                ])
            ])
        ]),
        dbc.Col(md=4, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3("60%", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Grupos que descartan locales sin opciones (Faunalytics)", style={"color": "#7f8c8d", "fontSize": "9.5pt"})
                ])
            ])
        ]),
        dbc.Col(md=4, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3(f"{len(df_render)}", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Establecimientos Analizados en el Pipeline", style={"color": "#7f8c8d", "fontSize": "9.5pt"})
                ])
            ])
        ]),
    ]),

    # SECCIÓN 2: EL DIAGNÓSTICO DE MERCADO (Plotly interactivo)
    dbc.Row(className="mb-5", children=[
        dbc.Col(md=12, children=[
            html.H3("1. Diagnóstico Geográfico: ¿Dónde está la oportunidad?", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px"}),
            html.P("Este gráfico interactivo permite al consultor identificar las ciudades con mayor precio promedio por plato, evaluando dónde el poder adquisitivo justifica el desarrollo de menús de autor.", style={"color": "#2c3e50"}),
            dbc.Card(style={"padding": "15px", "boxShadow": "0 4px 6px rgba(0,0,0,0.05)"}, children=[
                dcc.Graph(figure=grafico_barras(df_render, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO))
            ])
        ])
    ]),

    # SECCIÓN 3: ESTRUCTURACIÓN DE COSTOS (Matplotlib y Seaborn en paralelo)
    dbc.Row(className="mb-5", children=[
        html.H3("2. Ingeniería de Menús: Análisis de Márgenes y Dispersión", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px", "marginBottom": "20px"}),
        
        # Izquierda: cajas y bigotes
        dbc.Col(md=6, children=[
            dbc.Card(style={"padding": "15px", "height": "100%"}, children=[
                html.H5("Distribución de Precios por Categoría", style={"color": "#4a7564"}),
                html.P("Permite comparar si las opciones puramente veganas sostienen un precio competitivo frente a las alternativas vegetarianas tradicionales.", style={"fontSize": "9.5pt", "color": "#7f8c8d"}),
                html.Img(
                    src=IMG_BASE64.format(cajas_y_bigotes(df_render, Restaurante.COL_PRECIO, Restaurante.COL_TIPO)),
                    style={"width": "100%", "borderRadius": "5px"}
                )
            ])
        ]),
total_locales = len(df_final_mercado)
precio_promedio_global = round(df_final_mercado[Restaurante.COL_PRECIO].mean(), 2)

app.layout = html.Div(
    [
        html.H1("Plataforma Analítica de Inteligencia Gastronómica Plant-Based", style={'color': '#1b4d3e', 'textAlign': 'center'}),
        html.P("Herramienta interactiva y estática para la toma de decisiones en consultoría de menús veganos.", style={'textAlign': 'center'}),
        html.Div(
    [
        html.Div(
            [
                html.H3(f"{total_locales}", style={"color": "#1b4d3e", "margin": "0"}),
                html.P("Locales Competidores Analizados", style={"margin": "0", "fontSize": "14px"})
            ],
            style={"border": "2px solid #8fbc8f", "padding": "15px", "borderRadius": "8px", "backgroundColor": "#eef5f2", "textAlign": "center", "width": "45%"}
        ),
        html.Div(
            [
                html.H3(f"${precio_promedio_global} USD", style={"color": "#1b4d3e", "margin": "0"}),
                html.P("Precio Promedio General", style={"margin": "0", "fontSize": "14px"})
            ],
            style={"border": "2px solid #8fbc8f", "padding": "15px", "borderRadius": "8px", "backgroundColor": "#eef5f2", "textAlign": "center", "width": "45%"}
        ),
    ],
    style={"display": "flex", "justify-content": "space-around", "margin": "20px 0"}
),
        
        html.H2("Análisis Estático de Precios (Matplotlib)"),
        html.P("Muestra la distribución de precios y los rangos de mercado de la oferta vegana vs vegetariana:"),
        html.Div(
            [
                html.Img(
                    src=IMG_BASE64.format(
                        cajas_y_bigotes(df_render, Restaurante.COL_PRECIO, Restaurante.COL_TIPO)
                    ),
                    style={"max-width": "80%", "height": "auto", "margin": "0 auto"}
                )
            ],
            style={"textAlign": "center", "margin-bottom": "30px"} # Centra la imagen y le da espacio abajo
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
                            {"bottom": 0, "left": 0, "right": len(df_render), "top": df_render[Restaurante.COL_PRECIO].max() + 5}
                        )
                    ),
                    style={"max-width": "80%", "margin": "0 auto"} # Lo centra y le da un tamaño armónico
                )
            ],
            style={"textAlign": "center"},
        ),
        
        # Derecha: gráfico de dispersión Seaborn
        dbc.Col(md=6, children=[
            dbc.Card(style={"padding": "15px", "height": "100%"}, children=[
                html.H5("Tendencias y Líneas de Regresión", style={"color": "#4a7564"}),
                html.P("Mapeo de la estabilidad de precios para detectar anomalías o nichos de mercado sub-explotados.", style={"fontSize": "9.5pt", "color": "#7f8c8d"}),
                html.Img(
                    src=IMG_BASE64.format(dispersion(df_render, Restaurante.COL_TIPO, 'indice_registro', Restaurante.COL_PRECIO)),
                    style={"width": "100%", "borderRadius": "5px"}
                )
            ])
        ])
    ]),
    
    # PIE DE PÁGINA
    dbc.Row(children=[
        dbc.Col(style={"color": "#7f8c8d", "fontSize": "9pt", "marginTop": "20px", "textAlign": "center"}, children=[
            html.P("© 2026 - Proyecto Académico de Ciencia de Datos Aplicada a la Consultoría Gastronómica Plant-Based")
        ])
    ])
])
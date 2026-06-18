from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from data_processing import df_final_mercado
from esquema.restaurante import Restaurante
from vista.matplotlib_utils import cajas_y_bigotes
from vista.seaborn_utils import dispersion
from vista.plotly_utils import grafico_barras

# Inicio 
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

IMG_BASE64 = "data:image/png;base64,{}"

df_render = df_final_mercado.copy()
df_render['indice_registro'] = range(len(df_render))

# --- CÁLCULO DE MÉTRICAS COMPLEMENTARIAS  ---
total_locales = len(df_final_mercado)
precio_promedio_global_usd = round(df_final_mercado[Restaurante.COL_PRECIO].mean(), 2)


if Restaurante.COL_PRECIO_ARS in df_final_mercado.columns:
    precio_promedio_global_ars = df_final_mercado[Restaurante.COL_PRECIO_ARS].mean()
    precio_maximo_ars = df_final_mercado[Restaurante.COL_PRECIO_ARS].max()
""" else:
    tasa_proxy = 1455.0
    precio_promedio_global_ars = df_final_mercado[Restaurante.COL_PRECIO].mean() * tasa_proxy
    precio_maximo_ars = df_final_mercado[Restaurante.COL_PRECIO].max() * tasa_proxy """

# --- CONTENEDOR PRINCIPAL  ---
app.layout = dbc.Container(fluid=True, style={"backgroundColor": "#fcfcfc", "padding": "30px"}, children=[
    
    # ENCABEZADO PRINCIPAL (Introducción al problema)
    dbc.Row(className="mb-5", children=[
        dbc.Col(style={"textAlign": "center"}, children=[
            html.H1("Plataforma de inteligencia en gastronomía vegana en Argentina", 
                    style={"color": "#1b4d3e", "fontWeight": "bold", "fontSize": "28pt"}),
            html.H5("Análisis de oportunidades de negocio mediante Ciencia de Datos", 
                    style={"color": "#618274", "fontStyle": "italic"}),
            html.Hr(style={"borderColor": "#8fbc8f", "borderWidth": "2px", "width": "60%", "margin": "auto"})
        ])
    ]),

    # SECCIÓN 1: KPIs MACRO REUNIDOS
    dbc.Row(className="mb-4 text-center", children=[
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3("12.4%", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Crecimiento anual del mercado (Fuente: Grand View Research)", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3("60%", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Tasa de deserción por comensal veto (Fuente: Faunalytics)", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3(f"{total_locales}", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Locales competidores analizados", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3(f"${precio_promedio_global_usd} USD", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Precio promedio general", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ])
    ]),

    # SECCIÓN DE NUEVOS KPIs (Kaggle Nutritional Patterns)
    dbc.Row(className="mb-5 text-center", children=[
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#f4f9f6", "border": "1px dashed #1b4d3e"}, children=[
                dbc.CardBody([
                    html.H3(f"${precio_promedio_global_ars:,.2f}", style={"color": "#4a7564", "fontWeight": "bold"}),
                    html.P("Precio promedio (ARS)", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#f4f9f6", "border": "1px dashed #1b4d3e"}, children=[
                dbc.CardBody([
                    html.H3(f"${precio_maximo_ars:,.2f}", style={"color": "#4a7564", "fontWeight": "bold"}),
                    html.P("Precio techo de mercado (ARS)", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#e8f0ec", "border": "1px solid #8fbc8f"}, children=[
                dbc.CardBody([
                    html.H3("-35%", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Eficiencia en costo de insumos crudos", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#e8f0ec", "border": "1px solid #8fbc8f"}, children=[
                dbc.CardBody([
                    html.H3("0%", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Grasas Saturadas y Colesterol Base", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ])
    ]),

    # SECCIÓN 2: EL DIAGNÓSTICO DE MERCADO (Plotly interactivo)
    dbc.Row(className="mb-5", children=[
        dbc.Col(md=12, children=[
            html.H3("1. Diagnóstico geográfico: ¿Dónde está la oportunidad?", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px"}),
            html.P("Este gráfico interactivo permite al consultor identificar las ciudades con mayor precio promedio por plato, evaluando dónde el poder adquisitivo justifica el desarrollo de menúes de autor.", style={"color": "#2c3e50"}),
            dbc.Card(style={"padding": "15px", "boxShadow": "0 4px 6px rgba(0,0,0,0.05)"}, children=[
                dcc.Graph(figure=grafico_barras(df_render, Restaurante.COL_CIUDAD, Restaurante.COL_PRECIO))
            ])
        ])
    ]),

    # SECCIÓN 3: ESTRUCTURACIÓN DE COSTOS (Matplotlib y Seaborn en paralelo)
    dbc.Row(className="mb-5", children=[
        html.H3("2. Ingeniería de menúes: Análisis de márgenes y dispersión", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px", "marginBottom": "20px"}),
        
        # Izquierda: cajas y bigotes (Matplotlib)
        dbc.Col(md=6, children=[
            dbc.Card(style={"padding": "15px", "height": "100%"}, children=[
                html.H5("Distribución de precios por categoría", style={"color": "#4a7564"}),
                html.P("Permite comparar si las opciones puramente veganas sostienen un precio competitivo frente a las alternativas vegetarianas tradicionales.", style={"fontSize": "9.5pt", "color": "#7f8c8d"}),
                html.Div([
                    html.Img(
                        src=IMG_BASE64.format(cajas_y_bigotes(df_render, Restaurante.COL_PRECIO, Restaurante.COL_TIPO)),
                        style={"width": "100%", "borderRadius": "5px"}
                    )
                ], style={"textAlign": "center"})
            ])
        ]),
        
        # Derecha: gráfico de dispersión (Seaborn)
        dbc.Col(md=6, children=[
            dbc.Card(style={"padding": "15px", "height": "100%"}, children=[
                html.H5("Tendencias y líneas de regresión", style={"color": "#4a7564"}),
                html.P("Mapeo de la estabilidad de precios para detectar anomalías o nichos de mercado.", style={"fontSize": "9.5pt", "color": "#7f8c8d"}),
                html.Div([
                    html.Img(
                        src=IMG_BASE64.format(dispersion(df_render, Restaurante.COL_TIPO, 'indice_registro', Restaurante.COL_PRECIO)),
                        style={"width": "100%", "borderRadius": "5px"}
                    )
                ], style={"textAlign": "center"})
            ])
        ])
    ]),

    # PIE DE PÁGINA
    dbc.Row(children=[
        dbc.Col(style={"color": "#7f8c8d", "fontSize": "9pt", "marginTop": "20px", "textAlign": "center"}, children=[
            html.P("© 2026 - Proyecto académico de POAD para la consultoría gastronómica vegana")
        ])
    ])
])
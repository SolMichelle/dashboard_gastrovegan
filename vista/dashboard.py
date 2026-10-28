from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from data_processing import df_final_mercado, df_argentina, df_platos, datos_argentina
from esquema.restaurante import Restaurante
from vista.matplotlib_utils import cajas_y_bigotes
from vista.seaborn_utils import dispersion
from vista.plotly_utils import generar_grafico_barras_argentina

# Importamos las funciones del nuevo backend analítico 
from backend_analitica import (
    entrenar_modelo_rentabilidad, 
    analisis_estadistico_ejecutivo, 
    procesar_datos_nutricionales
)
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

IMG_BASE64 = "data:image/png;base64,{}"

df_render = df_final_mercado.copy()
df_render['indice_registro'] = range(len(df_render))

# --- CÁLCULOS MONETARIOS ---
total_locales = len(df_final_mercado)
precio_promedio_global_usd = round(df_final_mercado[Restaurante.COL_PRECIO].mean(), 2)
precio_promedio_global_ars = df_final_mercado[Restaurante.COL_PRECIO_ARS].mean()
precio_maximo_ars = df_final_mercado[Restaurante.COL_PRECIO_ARS].max()

# --- CARGA DE MODELOS Y DATOS ANALÍTICOS ---
_, accuracy_modelo = entrenar_modelo_rentabilidad()
resumen_stat = analisis_estadistico_ejecutivo()
df_nutricion = procesar_datos_nutricionales()

# Gráfico nutricional interactivo basado en Food_and_Nutrition.csv
if not df_nutricion.empty and 'protein' in df_nutricion.columns:
    fig_nutricion = px.box(
        df_nutricion, 
        x='dieta_es', 
        y='protein', 
        color='dieta_es',
        title="Comparativa de Aporte Proteico por Tipo de Dieta (g)",
        labels={'dieta_es': 'Tipo de Dieta', 'protein': 'Proteína (g)'},
        color_discrete_map={'Vegana': '#1b4d3e', 'Vegetariana': '#8fbc8f', 'Omnívora': '#2c3e50'}
    )
    fig_nutricion.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
else:
    fig_nutricion = px.bar(title="Datos nutricionales en proceso de sincronización")


# --- LAYOUT DE LA PESTAÑA 1  ---
pestana_1_layout = html.Div([
    # ENCABEZADO PRINCIPAL
    dbc.Row(className="mb-5", children=[
        dbc.Col(style={"textAlign": "center"}, children=[
            html.H1("Plataforma de inteligencia de datos sobre gastronomía vegana", 
                    style={"color": "#1b4d3e", "fontWeight": "bold", "fontSize": "28pt"}),
            html.H5("Análisis multifuente de viabilidad comercial y costos", 
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
                    html.P("Locales analizados", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ]),
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#eef5f2", "border": "1px solid #cce2d7"}, children=[
                dbc.CardBody([
                    html.H3(f"${precio_promedio_global_usd} USD", style={"color": "#1b4d3e", "fontWeight": "bold"}),
                    html.P("Precio promedio internacional", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ])
    ]),

    # KPIs EN PESOS ARS & NUTRICIONALES
    dbc.Row(className="mb-5 text-center", children=[
        dbc.Col(md=3, children=[
            dbc.Card(style={"backgroundColor": "#f4f9f6", "border": "1px dashed #1b4d3e"}, children=[
                dbc.CardBody([
                    html.H3(f"${precio_promedio_global_ars:,.2f}", style={"color": "#4a7564", "fontWeight": "bold"}),
                    html.P("Precio promedio equivalente (ARS)", style={"color": "#7f8c8d", "fontSize": "9pt"})
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
                    html.P("Grasas saturadas y colesterol base", style={"color": "#7f8c8d", "fontSize": "9pt"})
                ])
            ])
        ])
    ]),

    # GRÁFICO INTERACTIVO - FACTIBILIDAD ARGENTINA
    dbc.Row(className="mb-5", children=[
        dbc.Col(md=12, children=[
            html.H3("1. Estudio de geomarketing: factibilidad sociodemográfica regional", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px"}),
            html.P("Este gráfico interactivo procesa los datos de densidad y poder adquisitivo estimado.", style={"color": "#2c3e50"}),
            dbc.Card(style={"padding": "15px"}, children=[
                dcc.Graph(figure=generar_grafico_barras_argentina(df_argentina))
            ])
        ])
    ]),

    # SECCIÓN: INGENIERÍA DE COSTOS (MATPLOTLIB Y SEABORN ESTÁTICOS)
    dbc.Row(className="mb-5", children=[
        html.H3("2. Análisis técnico de costos y tendencias en pesos", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px", "marginBottom": "20px"}),
        
        dbc.Col(md=6, children=[
            dbc.Card(style={"padding": "15px"}, children=[
                html.H5("Distribución de rangos", style={"color": "#4a7564"}),
                html.Img(src=IMG_BASE64.format(cajas_y_bigotes(df_render, Restaurante.COL_PRECIO_ARS, Restaurante.COL_TIPO)))
            ])
        ]),
        dbc.Col(md=6, children=[
            dbc.Card(style={"padding": "15px"}, children=[
                html.H5("Línea de tendencia adaptada", style={"color": "#4a7564"}),
                html.Img(src=IMG_BASE64.format(dispersion(df_render, Restaurante.COL_TIPO, 'indice_registro', Restaurante.COL_PRECIO_ARS, {"bottom": 0, "top": df_render[Restaurante.COL_PRECIO_ARS].max() + 5000})))
            ])
        ])
    ]),

    # SECCIÓN: TABLA DE DATOS PANDAS DE PLATOS VEGANIZABLES
    dbc.Row(className="mb-5", children=[
        dbc.Col(md=12, children=[
            html.H3("3. Catálogo técnico: opciones tradicionales optimizadas de bajo costo", style={"color": "#1b4d3e", "borderLeft": "5px solid #8fbc8f", "paddingLeft": "10px"}),
            html.P("Matriz analítica de los 20 platos de la cultura argentina seleccionados para ser adaptados empleando aglutinantes y técnicas alternativas sin alterar el costo de producción.", style={"color": "#2c3e50"}),
            dbc.Card(style={"padding": "20px"}, children=[
                dash_table.DataTable(
                    data=df_platos.to_dict('records'),
                    columns=[
                        {"name": "Plato tradicional", "id": "plato"},
                        {"name": "Ingrediente de reemplazo sugerido", "id": "ingrediente_reemplazo"},
                        {"name": "Costo estimado de insumos (ARS)", "id": "costo_insumos_ars", "type": "numeric"},
                        {"name": "Categoría de menú", "id": "categoria"}
                    ],
                    style_header={'backgroundColor': '#1b4d3e', 'color': 'white', 'fontWeight': 'bold', 'textAlign': 'center'},
                    style_cell={'padding': '10px', 'textAlign': 'left', 'fontFamily': 'sans-serif', 'fontSize': '11pt'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f9fbf9'}],
                    page_size=10 
                )
            ])
        ])
    ])
])


# --- LAYOUT DE LA PESTAÑA 2  ---
pestana_2_layout = html.Div([
    html.H3("Módulo de IA, pronóstico y nutrición", style={"color": "#1b4d3e", "marginBottom": "20px"}),
    
    # Fila de indicadores de ML y Estadística
    dbc.Row(className="mb-4", children=[
        dbc.Col(md=6, children=[
            dbc.Card(style={"border": "1px solid #1b4d3e"}, children=[
                dbc.CardHeader("Predicción de rentabilidad", style={"backgroundColor": "#1b4d3e", "color": "white", "fontWeight": "bold"}),
                dbc.CardBody([
                    html.H2(f"{accuracy_modelo * 100:.1f}%", style={"color": "#1b4d3e", "textAlign": "center", "fontWeight": "bold"}),
                    html.P("Precisión del modelo de clasificación para predecir si un menú optimizado se ubica en el rango de alta rentabilidad en función de sus costos.", style={"color": "#2c3e50", "fontSize": "10pt"})
                ])
            ])
        ]),
        dbc.Col(md=6, children=[
            dbc.Card(style={"border": "1px solid #8fbc8f"}, children=[
                dbc.CardHeader("Pronóstico y validación estadística", style={"backgroundColor": "#8fbc8f", "color": "#1b4d3e", "fontWeight": "bold"}),
                dbc.CardBody([
                    html.H5(f"Margen promedio estimado: {resumen_stat['margen_medio']}%", style={"color": "#1b4d3e"}),
                    html.P(resumen_stat['conclusion'], style={"color": "#2c3e50", "fontSize": "10pt"})
                ])
            ])
        ])
    ]),

    # Sección de análisis nutricional (Food_and_Nutrition.csv)
    dbc.Row(className="mb-5", children=[
        dbc.Col(md=12, children=[
            dbc.Card(style={"padding": "15px"}, children=[
                dcc.Graph(figure=fig_nutricion)
            ])
        ])
    ]),

    html.Hr(style={"borderColor": "#8fbc8f"}),

    # Buscador interactivo
    dbc.Row(className="mb-5", children=[
        dbc.Col(md=12, children=[
            html.H4("Buscador opciones y costos de insumos", style={"color": "#1b4d3e"}),
            html.P("Ingrese un término (ej: lentejas, papa, empanadas) para consultar alternativas y costos en ARS:", style={"color": "#2c3e50"}),
            dcc.Input(
                id='input-buscador-ingrediente',
                type='text',
                placeholder='Buscar plato o ingrediente...',
                className='form-control mb-4 w-50'
            ),
            html.Div(id='contenedor-tabla-resultados')
        ])
    ])
])


# --- ENSAMBLE PRINCIPAL DE LA APLICACIÓN CON PESTAÑAS ---
app.layout = dbc.Container(fluid=True, style={"backgroundColor": "#fcfcfc", "padding": "30px"}, children=[
    
    dcc.Tabs(id="tabs-principales", value='tab-1', children=[
        dcc.Tab(label='Diagnóstico', value='tab-1', children=[pestana_1_layout],
                style={'fontWeight': 'bold', 'color': '#1b4d3e'}, selected_style={'fontWeight': 'bold', 'backgroundColor': '#eef5f2', 'color': '#1b4d3e'}),
        dcc.Tab(label='Analítica avanzada', value='tab-2', children=[pestana_2_layout],
                style={'fontWeight': 'bold', 'color': '#1b4d3e'}, selected_style={'fontWeight': 'bold', 'backgroundColor': '#eef5f2', 'color': '#1b4d3e'}),
    ]),

    # PIE DE PÁGINA COMÚN
    dbc.Row(children=[
        dbc.Col(style={"color": "#7f8c8d", "fontSize": "9pt", "marginTop": "40px", "textAlign": "center"}, children=[
            html.Hr(),
            html.P("© 2026 - Proyecto académico de la cátedra POAD para la consultoría gastronómica vegana")
        ])
    ])
])


# --- CALLBACK PARA EL BUSCADOR INTERACTIVO EN LA PESTAÑA 2 ---
@callback(
    Output('contenedor-tabla-resultados', 'children'),
    Input('input-buscador-ingrediente', 'value')
)
def actualizar_busqueda_platos(busqueda):
    if not busqueda:
        return html.P("Escriba en el campo superior para filtrar el catálogo técnico.", style={"color": "#7f8c8d", "fontStyle": "italic"})
    
    mask = (
        df_platos['plato'].str.contains(busqueda, case=False, na=False) | 
        df_platos['ingrediente_reemplazo'].str.contains(busqueda, case=False, na=False)
    )
    df_filtrado = df_platos[mask]
    
    if df_filtrado.empty:
        return html.P("No se encontraron coincidencias para la búsqueda especificada en el catálogo.", style={"color": "#c0392b"})
    
    return dash_table.DataTable(
        data=df_filtrado.to_dict('records'),
        columns=[
            {"name": "Plato tradicional", "id": "plato"},
            {"name": "Ingrediente de reemplazo sugerido", "id": "ingrediente_reemplazo"},
            {"name": "Costo estimado de insumos (ARS)", "id": "costo_insumos_ars", "type": "numeric"},
            {"name": "Categoría de menú", "id": "categoria"}
        ],
        style_header={'backgroundColor': '#1b4d3e', 'color': 'white', 'fontWeight': 'bold', 'textAlign': 'center'},
        style_cell={'padding': '10px', 'textAlign': 'left', 'fontFamily': 'sans-serif', 'fontSize': '11pt'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f9fbf9'}],
        page_size=5 
    )
import plotly.express as px

def generar_grafico_barras_argentina(dataframe):
    # Genera un gráfico interactivo 
    fig = px.bar(
        dataframe,
        x="provincia_ciudad",
        y="score_inversion",
        text="score_inversion",
        title="Índice de oportunidad de inversión por ciudad",
        labels={
            "provincia_ciudad": "Ciudad / Región",
            "score_inversion": "Score de Viabilidad (Densidad × Poder Adquisitivo)"
        },
        color="score_inversion",
        color_continuous_scale="Mint" 
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#2c3e50"
    )
    return fig
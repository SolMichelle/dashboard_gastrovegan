# Instalaciones requeridas: pip install pandas plotly dash dash-bootstrap-components matplotlib seaborn
from vista.dashboard import app

def main():
    # Ejecuta el servidor local de Dash en http://127.0.0.1:8050
    app.run(debug=True)

if __name__ == "__main__":
    main()
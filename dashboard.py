import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
import json
import os

# Charger les données
def load_prices():
    try:
        df = pd.read_csv("prices.csv", names=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")
        return df
    except:
        return pd.DataFrame(columns=["timestamp", "price"])

def load_report():
    if os.path.exists("daily_report.json"):
        with open("daily_report.json") as f:
            return json.load(f)
    return {"status": "vide"}

# Initialisation de l'app
app = dash.Dash(__name__)
app.title = "Ethereum Dashboard"

app.layout = html.Div([
    html.H1("Ethereum Price Dashboard", style={"textAlign": "center"}),

    html.Div(id="current-price", style={"fontSize": "24px", "textAlign": "center", "marginTop": "20px"}),

    dcc.Graph(id="price-graph"),

    html.H2("Rapport quotidien", style={"marginTop": "40px", "textAlign": "center"}),

    html.Div(id="daily-report", style={"textAlign": "center", "fontSize": "18px", "marginBottom": "40px"})
])

@app.callback(
    dash.dependencies.Output("current-price", "children"),
    dash.dependencies.Output("price-graph", "figure"),
    dash.dependencies.Output("daily-report", "children"),
    dash.dependencies.Input("price-graph", "id")
)
def update_dashboard(_):
    df = load_prices()
    report = load_report()

    if df.empty:
        current_price = "Aucune donnée disponible"
        fig = go.Figure()
    else:
        last_price = df.iloc[-1]["price"]
        current_price = f"Dernier prix ETH : {last_price:.2f} $"
        fig = go.Figure(data=[go.Scatter(x=df["timestamp"], y=df["price"], mode="lines+markers")])
        fig.update_layout(title="Évolution ETH/USD", xaxis_title="Temps", yaxis_title="Prix ($)")

    if report.get("status") == "ok":
        report_text = html.Ul([
            html.Li(f"Date : {report['date']}"),
            html.Li(f"Prix d'ouverture : {report['open_price']} $"),
            html.Li(f"Prix de clôture : {report['close_price']} $"),
            html.Li(f"Variation : {report['variation_abs']} $ ({report['variation_pct']} %)"),
            html.Li(f"Volatilité : {report['volatility']}")
        ])
    else:
        report_text = "Aucun rapport disponible pour aujourd'hui."

    return current_price, fig, report_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)

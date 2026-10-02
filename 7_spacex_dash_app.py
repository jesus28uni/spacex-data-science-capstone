import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

app = dash.Dash(__name__)
sites = [{"label": "Todos los sitios", "value": "ALL"}] + [
    {"label": s, "value": s} for s in spacex_df["Launch Site"].unique()]

app.layout = html.Div([
    html.H1("Panel de lanzamientos de SpaceX", style={"textAlign": "center", "color": "#503D36", "fontSize": 40}),
    dcc.Dropdown(id="site-dropdown", options=sites, value="ALL",
                 placeholder="Selecciona un sitio de lanzamiento", searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.P("Rango de carga útil (kg):"),
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)}, value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])

@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def get_pie_chart(site):
    if site == "ALL":
        return px.pie(spacex_df, values="class", names="Launch Site", title="Éxitos totales por sitio")
    df = spacex_df[spacex_df["Launch Site"] == site]
    counts = df["class"].value_counts().reset_index()
    counts.columns = ["class", "count"]
    return px.pie(counts, values="count", names="class", title=f"Éxitos vs fallos en {site}")

@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def get_scatter(site, payload):
    low, high = payload
    df = spacex_df[spacex_df["Payload Mass (kg)"].between(low, high)]
    if site != "ALL":
        df = df[df["Launch Site"] == site]
    return px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                      title="Carga útil vs resultado del lanzamiento")

if __name__ == "__main__":
    app.run(debug=True)

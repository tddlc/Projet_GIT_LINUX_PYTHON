from dash import Dash, html, dcc, dependencies
import plotly.express as px
import pandas as pd
import os
import datetime as dt

app = Dash(__name__)
#make the app darkmode
app.title = "Cours de Nike (NKE)"

last_modified = 0
df = None

def load_data():
    df = pd.read_csv("table.csv",sep=";", parse_dates=["Date"], dayfirst=True)
    last_modified = os.path.getmtime("table.csv")
    return df

def create_figure():
    fermeture = px.line(df, x="Date", y="Dernier", title='Prix de fermeture au cours du temps')
    ouverture = px.line(df, x="Date", y="Ouv.", title='Prix d\'ouverture au cours du temps')
    volume = px.line(df, x="Date", y="Vol.", title='Volume au cours du temps')
    return [fermeture, ouverture, volume]

@app.callback(dependencies.Output('graph-fermeture', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_fermeture(n):
    if last_modified != os.path.getmtime("table.csv"):
        df = load_data()
        fermeture = create_figure()[0]
        return fermeture
    return fermeture

@app.callback(dependencies.Output('graph-ouverture', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_ouverture(n):
    if last_modified != os.path.getmtime("table.csv"):
        df = load_data()
        ouverture= create_figure()[1]
        return ouverture 
    return ouverture 

@app.callback(dependencies.Output('graph-volume', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_volume(n):
    if last_modified != os.path.getmtime("table.csv"):
        df = load_data()
        volume= create_figure()[2]
        return volume 
    return volume
if __name__ == '__main__':
    df = load_data()
    fermeture,ouverture,volume= create_figure()

    app.layout = html.Div(children=[
        html.H1(children='Cours de Nike (NKE)', style={'textAlign': 'center'}),

        dcc.Graph(
            id='graph-fermeture',
            figure=fermeture
        ),
        dcc.Graph(
            id='graph-ouverture',
            figure=ouverture
        ),
        dcc.Graph(
            id='graph-volume',
            figure=volume
            ),

        dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
    ])
    app.run_server(debug=True,host="172.31.60.11",port=8050)

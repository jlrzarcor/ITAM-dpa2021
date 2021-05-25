# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pickle as pkl
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
predic = pkl.load(open("df_predic.pkl", "rb"))

fig = px.histogram(predic, x="prediction", color="prediction")


app.layout = html.Div(children=[
    html.H1(children='Distribución de scores de nuetra predicción'),

    html.Div(children='''
        El dataframe tiene un total de 200 registros.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
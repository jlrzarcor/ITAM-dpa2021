# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

import plotly.graph_objects as go
from plotly.subplots import make_subplots

user = 'octavio'
password = 'alan'
host = 'rds-dpa-project.cudydvgqgf80.us-west-2.rds.amazonaws.com'
port = '5432'
dbname = 'chicagofoodinsp'
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, dbname)

connection = create_engine(url)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

query_1 = 'SELECT * FROM api.dash;'

df_query = pd.read_sql_query(query_1, connection)

fig = px.histogram(df_query, x="score")
fig2 = px.histogram(df_query, x="score")

app.layout = html.Div(children=[
    html.Div([
    html.H1(children='Distribución de scores de nuestra predicción'),

    html.Div(children='''
        DPA.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Distribución de scores de nuestra predicción 2'),

        html.Div(children='''
            DPA.
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

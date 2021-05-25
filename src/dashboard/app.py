### Chicago Food Inspections, scores model vs consecutive API.
### ITAM, Data Product Arquitecture, Spring 2021.
### Paty Urriza, Octavio Fuentes, Uriel Rangel, Carlos Román, José Luis R. Zárate

# ================================= LIBRARIES  ================================= #

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Special routing for importing custom libraries

# Modify path
old_path = os.getcwd()
path = os.path.realpath('../..')

# Get imports
from src.utils.general import get_pg_service
pg = get_pg_service(path + '/conf/local/credentials.yaml')

#import src.utils.constants as ks
#from src.utils.general import get_db_conn_sql_alchemy

# Reset path
os.path.realpath(old_path)


# ================================= API ================================= #

# Connection to RDS-Postgress chicagofoodinsp db
url = 'postgresql://{}:{}@{}:{}/{}'.format(pg['user'], pg['password'], pg['host'], str(pg['port']), pg['dbname'])
connection = create_engine(url)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

query_c = "Select * FROM dsh.model WHERE tipo = 'c' AND ingest_date = (select max(ingest_date) from dsh.model where tipo = 'c')"
query_m = "Select * FROM dsh.model WHERE tipo = 'm' AND ingest_date = (select max(ingest_date) from dsh.model where tipo = 'm')"
#query_m = "SELECT score FROM schema.modelo WHERE date BETWEEN '"+ query_0 +"' AND '"+ query_0 +"' AND type = 'm';"

df_query_consec = pd.read_sql_query(query_c, connection)
df_query_model = pd.read_sql_query(query_m, connection)

fig = px.histogram(df_query_consec, x="score")
fig2 = px.histogram(df_query_model, x="score")

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

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import requests
import plotly.express as px
from dash.dependencies import Input, Output, State
import random
import dash_auth

USERNAME_PASSWORD_PAIRS= [['equipo55', 'team_55'],['equipo_55', 'team_555']]


# Import and clean data (importing csv into pandas)
user = 'ds4a_user'
password = 'b9tb5440'
host = 'ds4a-project.cwpujbafhcpo.us-east-2.rds.amazonaws.com'
port = '5432'
db = 'ds4a_proj'
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
con = create_engine(url)

query = "SELECT * FROM model"

df = pd.read_sql(query, con)
#------------------------------------------------------------------

# Set up Dashboard and create layout
app = dash.Dash()
auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server 

#define app layout
app.layout=html.Div([
    html.Div([
        html.Div([
            html.H1("Team 55: Quantum Spin", className="text-center", id="heading"),
            html.Img(src="/assets/team55.png")
        ], className = "banner"
        ),
    ],className="row"),
    html.Div(
        [
            html.Div([
                html.Div(
                    [
                        dcc.Dropdown(
                            options=[
                                {'label': 'Velocidad 20', 'value': 'Velocidad 20'},
                                {'label': 'Velocidad 40', 'value': 'Velocidad 40'},
                                {'label': 'Velocidad 60', 'value': 'Velocidad 60'},
                                {'label': 'Velocidad 80', 'value': 'Velocidad 80'}
                            ],
                            id='score-dropdown')], className="col-md-12"),
                html.Div(
                    html.Table(id='datatable', className = "table col-md-12")),],className="col-md-6"),
            html.Div(
                [dcc.Graph(id='line-graph',
                           figure=go.Figure(
                               data = [
                                   go.Scatter(
                                       x=df.City,
                                       y=df['Velocidad 40'],
                                       mode='markers',
                                       name='Velocidad 40'),
                                   go.Scatter(
                                       x = df.City,
                                       y = df['Velocidad 60'],
                                       mode = 'markers',
                                       name = 'Velocidad 60'),
                                   go.Scatter(
                                       x = df.City,
                                       y = df['Velocidad 80'],
                                       mode = 'markers',
                                       name = 'Velocidad 80'),],

                               layout=go.Layout(title="Selling speed")
                           )
                           ),
                 ], className = "col-md-6"
            ),
        ], className="row"),\
    html.Div(
        [
            html.Div(
                [dcc.Graph(id='bubble-chart',
                           figure=go.Figure(
                               data=[
                                   go.Scatter(
                                       x=df.Estrato,
                                       y=df.area_promedio,
                                       mode='markers',
                                       text=df.Proyecto,
                                       marker=dict(
                                           color= random.sample(range(1,200),15),
                                           size=df.Estrato,
                                           sizemode='area',
                                           sizeref=2.*max(df.Estrato),
                                           sizemin=4
                                       )
                                   )
                               ],
                               layout=go.Layout(title="Stratum")
                           )
                           )
                 ], className = "col-md-6"
            ),
            html.Div([
                dcc.Graph(id='bar-chart',
                          style={'margin-top': '20'})
            ], className = "col-md-6"
            ),
        ], className="row"),
    ],

className="container-fluid")


@app.callback(
	Output(component_id='datatable', component_property='children'),
	[Input(component_id='score-dropdown', component_property='value')]
	)
def  update_table(input_value):
	return generate_table(df.sort_values([input_value], ascending=[False]).reset_index())
@app.callback(
	Output(component_id='bar-chart', component_property='figure'),
	[Input(component_id='bubble-chart', component_property='hoverData')]
	)
def  update_graph(hoverData):
	return bar(hoverData)




if  __name__ == '__main__':
    app.run_server(debug=True)
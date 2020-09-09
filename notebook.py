import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import requests
import plotly.express as px
import random

from dash.dependencies import Input, Output, State

#----------------------------------------------------------------------------

# Import and clean data (importing csv into pandas)
df = pd.read_excel('')
# ------------------------------------------------------------------


# Set up Dashboard and create layout
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
# auth to upload the app on heroku
server = app.server

df1 = pd.read_excel('')

data_bolivar = px.data.gapminder().query("country == 'Colombia'")
fig1 = px.bar(df, x='City', y='precio_promedio')



fig3 = go.Figure(data=[go.Scatter(
    x=df1['area_promedio'], y=df1['City'],
    mode='markers')
])


app.layout = html.Div([

    html.Div([
        html.Div([
            html.H1("TEAM 55: QUANTUM SPIN", className="text-center", id="heading"),
            html.Img(src="/assets/team55.png")
        ], className="banner"
        ),
    ], className="container scalable"),
    html.Div(
        [
            html.Div([
                html.Div(
                    [
                        dcc.Dropdown(
                            options=[
                                {'label': 'Alcobas', 'value': 'Av. Alcobas'},
                                {'label': 'Baños', 'value': 'Av. Baños'},
                                {'label': 'Fecha inicio', 'value': 'Fecha inicio'},
                                {'label': 'Estrato', 'value': 'Estrato'},
                                {'label': 'Total Unidades Proyecto', 'value': 'Tot. Un. Proyecto'},
                                {'label': 'area promedio', 'value': 'area_promedio'},
                                {'label': 'precio promedio', 'value': 'precio_promedio'},
                                {'label': 'Velocidad 20', 'value': 'Velocidad 20'},
                                {'label': 'Velocidad 40', 'value': 'Velocidad 40'},
                                {'label': 'Velocidad 60', 'value': 'Velocidad 60'},
                                {'label': 'Velocidad 80', 'value': 'Velocidad 80'},
                                {'label': 'Velocidad 100', 'value': 'Velocidad 100'},
                                {'label': 'Salón Social', 'value': 'Salón Social'},
                                {'label': 'Ascensores por Torre', 'value': 'No. Ascensores x Torre'}

                            ],
                            optionHeight=35,
                            value='Velocidad 20',
                            multi=True,
                            clearable=False,
                            id='score-dropdown')], className="col-md-12"),
                html.Div(
                    html.Table(id='datatable', className="table col-md-12")), ], className="col-md-6"),
            html.Div([
                html.H3("GRAPH CHOSEN", className="text-center", id="title fig"),
                dcc.Graph(id='line-graph',

                           ),

                 ], className="col-md-6"
            ),
        ], className="row"),
    html.Div(
        [
            html.Div([
                html.H3("AVERAGE SQUARE FEET PER CITY", className="text-center", id="title fig 2"),
                dcc.Graph(id='bubble-chart',
                           figure=fig3,
                           )
                 ],
                className="col-md-6"
            ),
            html.Div([
                html.H3("AVERAGE PRICE PER CITY", className="text-center", id="title fig 1"),
                dcc.Graph(id='bar-chart',
                          figure=fig1,
                          style={'margin-top': '20'})


            ],
                className="col-md-6"
            ),


        ], className="row"),
],
    className="container-fluid")


@app.callback(
    Output(component_id='line-graph', component_property='figure'),
    [Input(component_id='score-dropdown', component_property='value')]
)

def update_graph(score_dropdown):
    dff = df1
    linechart=px.scatter(
        data_frame=dff,
        x=df['City'],
        y= score_dropdown
    )
    return (linechart)


layout = dict(
    plot_bgcolor="#282b38", paper_bgcolor="#282b38")
if __name__ == '__main__':
    app.run_server(debug=True)



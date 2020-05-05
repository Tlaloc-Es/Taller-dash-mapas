#-*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px

import pandas as pd
import numpy as np
import json

app = dash.Dash(__name__)

DF = pd.read_csv('./data/unc.csv')
YEARS_DF = DF['Año'].unique()
TIPOS_DE_DELITO = DF['Tipo de delito'].unique()

with open('./geo/mexico.geojson') as f:
    STATES = json.load(f)


app.layout = html.Div([
   dbc.FormGroup(
       [
           dbc.Label("Tipo de delito"),
           dcc.Dropdown(
               id="in-delito",
               value=TIPOS_DE_DELITO[0],
               options=[
                   {"label": col, "value": col} for col in DF['Tipo de delito'].unique()
               ]
           ),
       ]
   ),

   dcc.Slider(
       id='in-year-slider',
       min=0,
       max=len(YEARS_DF),
       marks={i: str(YEARS_DF[i]) for i in range(len(YEARS_DF))},
       value=0,
   ),
  
   dcc.Graph(id="delito-map")

])


@app.callback(
    dash.dependencies.Output('delito-map', 'figure'),
    [
        dash.dependencies.Input('in-delito', 'value'),
        dash.dependencies.Input('in-year-slider', 'value')
    ]
)
def update_delito(delito, year):
    global STATES
    global YEARS_DF
    global DF

    year = YEARS_DF[year]

    df = DF.copy()

    df = df[df['Año']==year]
    df = df[df['Tipo de delito']==delito]
    df = df.groupby('Entidad').sum()
    df = df.reset_index()

    fig = px.choropleth(
        df,
        geojson = STATES,
        locations='Entidad',
        featureidkey='properties.NOMGEO',
        color_continuous_scale=px.colors.sequential.Reds,
        color='Total'
    )

    fig.update_geos(fitbounds='locations', visible=True)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
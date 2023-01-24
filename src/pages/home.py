# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:42:11 2022

@author: rongx
"""

from dash import callback, register_page
from dash_extensions.enrich import Output, Input, State, html, dcc  # pip install dash-extensions
import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd

register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

aggregate_dropdown = dcc.Dropdown(id = 'aggregate_dropdown',
                                options=['Incremental', 'Cummulative'],
                                value = 'Incremental',
                                clearable=False,
                                persistence=True,
                                persistence_type='session')

detailed_dropdown = dcc.Dropdown(id = 'detailed_dropdown',
                                options=['Incremental', 'Cummulative'],
                                value = 'Incremental',
                                clearable=False,
                                persistence=True,
                                persistence_type='session')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([aggregate_dropdown], width=3)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='lgraph1_container', children=[]))
    ]),
    dbc.Row([
        dbc.Col([detailed_dropdown], width=3)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='lgraph2_container', children=[]))
    ])
], id = 'home_component', style = {'display': 'none'})

@callback(
    Output('lgraph1_container', 'children'),
    Output('home_component', 'style'),
    Input(aggregate_dropdown, 'value'),
    Input('store', 'data'),
)
def lgraph1(agg, data):
    
    if data is None:
        return [[], {'display': 'none'}]
    
    df = pd.DataFrame(data)
    
    if agg == "Incremental":
        
        fig1 = px.line(data_frame = df.groupby('period')['total_hours'].sum(),
                       labels = {'value': 'Billable Hours'},
                       markers = True,
                       height = 750)
        
    else:
        
        fig1 = px.line(data_frame = df.groupby('period')['total_hours'].sum().cumsum(),
                       labels = {'value': 'Billable Hours'},
                       markers = True,
                       height = 750)
    
    fig1.update_layout(showlegend=False)
    return [dcc.Graph(figure = fig1), {'display': 'block'}]

@callback(
    Output('lgraph2_container', 'children'),
    Input(detailed_dropdown, 'value'),
    Input('store', 'data'),
)
def lgraph2(agg, data):
    
    if data is None:
        return []
    
    df = pd.DataFrame(data)
    
    if agg == "Incremental":
        
        fig2 = px.line(data_frame = df.groupby(['period', 'name_fam_last_first'])['total_hours'].sum().to_frame().reset_index(),
                       x = 'period',
                       y = 'total_hours',
                       color = 'name_fam_last_first',
                       labels = {'value': 'Billable Hours'},
                       markers = True,
                       height = 750)
        
    else:
        
        dff = df.groupby(['period', 'name_fam_last_first'])['total_hours'].sum().to_frame().reset_index()
        dff['cum_sum'] = (dff.groupby('name_fam_last_first')['total_hours'].cumsum())
        
        fig2 = px.line(data_frame = dff,
                       x = 'period',
                       y = 'cum_sum',
                       color = 'name_fam_last_first',
                       labels = {'cum_sum': 'Billable Hours', 'name_fam_last_first': 'Name'},
                       markers = True,
                       height = 750)
    
    return dcc.Graph(figure = fig2)
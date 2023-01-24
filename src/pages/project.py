# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 01:12:43 2023

@author: rongx
"""

# package imports

import dash
from dash_extensions.enrich import dcc, callback, Output, Input, State, html
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas

dash.register_page(
    __name__,
    path='/project',
)

num_input = dbc.Input(type='number', value = 10, min=1,max=10, step=1)

invalid_warning = dbc.FormText(children='', color='danger')

detail_dropdown = dcc.Dropdown(id = 'detail_dropdown',
                                options=['Consultant', 'Period'],
                                value = 'Consultant',
                                clearable=False,
                                persistence=True,
                                persistence_type='session')

layout = dbc.Container([
    dbc.Row([
        dbc.Label('Number of projects displayed: ', width='auto'),
        dbc.Col(
            [num_input],
            width='auto'
            ),

    ]),
    dbc.Row([
        dbc.Col(
            [invalid_warning],
            width='auto',
            )            
    ]),
    dbc.Row([
        dbc.Col([detail_dropdown], width=6, style={'margin-top': '10px'})
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='bgraph1_container', children=[]))
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="proj_container", children=[]), width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='bgraph2_container', children=[]))
    ])
], id = 'project_component', style = {'display': 'none'})

@callback(
    Output('bgraph1_container', 'children'),
    Output(num_input, 'max'),
    Output('project_component', 'style'),
    Input(num_input, 'value'),
    Input(detail_dropdown, 'value'),
    Input('store', 'data'),
)
def lgraph1(num_input, detail, data):
    
    if data is None:
        return [[], 10, {'display': 'none'}]
    
    df = pd.DataFrame(data)
    
    # to determine the top number of projects.
    hours_df = df.groupby('project_code', as_index=False).agg(total_hours=('total_hours', 'sum'))
    hours_df.sort_values(by='total_hours', ascending=False, inplace=True)
    top_proj = hours_df.project_code.iloc[:num_input]
    
    # count the number of projects
    num_proj = hours_df.project_code.nunique()
    
    # define how to aggregate various fields
    agg_functions = {'name': 'first', 'description': 'first', 'total_hours': 'sum'}
    
    # plot the graph with 
    if detail == 'Consultant':
        
        # extract relevent column
        dff = df[df['project_code'].isin(top_proj)].sort_values(by='period')[['project_code', 'total_hours', 'name_fam_last_first', 'name', 'description']]
        
        
                                                                     
        fig1 = px.bar(data_frame=dff.groupby(['project_code', 'name_fam_last_first'], as_index=False).aggregate(agg_functions), 
                      y='project_code', 
                      x='total_hours',
                      color='name_fam_last_first',
                      labels={'total_hours': 'Billable Hours', 'name_fam_last_first': 'Name'},
                      hover_name='name', #not working with histogram, need to use px.bar
                      hover_data=['description'],
                      height = 750)
        
    else:
        
        # extract relevent column
        dff = df[df['project_code'].isin(top_proj)].sort_values(by='period')[['project_code', 'total_hours', 'period', 'name', 'description']]

        fig1 = px.bar(data_frame=dff.groupby(['project_code', 'period'], as_index=False).aggregate(agg_functions), 
                      y='project_code', 
                      x='total_hours',
                      color='period',
                      labels={'total_hours': 'Billable Hours', 'name_fam_last_first': 'Name'},
                      hover_name='name',
                      hover_data=['description'],
                      height = 750)
        
    fig1.update_layout(yaxis = {'categoryorder':'total ascending'})
        
    return [dcc.Graph(figure = fig1), num_proj, {'display': 'block'}]

# generate warning if number inputed is inavalid
@callback(
    Output(invalid_warning, 'children'),
    Input(num_input, 'value'),
    State(num_input, 'max')  
)
def warning(value, maximum):
    if value is None:
        return f'Please type an integer within the range 1-{maximum}'
    else:
        ''

# generate values for dropdown
@callback(
    Output('proj_container', 'children'),
    Input('store', 'data')
)
def init_graph(data):
    if data is None:
        return []
    
    df = pd.DataFrame(data)
    cons_name = df['project_code'].unique()
    return dcc.Dropdown(id='proj_dropdown',
                        options= cons_name,
                        value=cons_name[0],  # initial value displayed when page first loads
                        clearable=False,
                        persistence=True,
                        persistence_type='session')

# plot graph
@callback(
    Output('bgraph2_container', 'children'),
    Input('proj_dropdown', 'value'),
    State('store', 'data')
)
def update_graph(proj_code, data):  # function arguments come from the component property of the Input    
    df = pd.DataFrame(data)
    
    if proj_code is None:
        return {}
    
    fig2 = px.bar(data_frame=df[df['project_code']==proj_code],
                  y='total_hours', 
                  x='period',
                  color='name_fam_last_first',
                  labels={'total_hours': 'Billable Hours', 'name_fam_last_first': 'Name'},
                  hover_name='name',
                  hover_data=['description'],
                  height = 750)
    
    fig2.update_xaxes(categoryorder='category ascending')
    
    return dcc.Graph(figure = fig2)
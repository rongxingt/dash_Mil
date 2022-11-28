# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:55:55 2022

@author: rongx
"""

# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas

# import the required file 
file_path = "Time_client code and consultant hours list - Jan-Jun'22.xlsx"
df = pd.read_excel(file_path)

# Data exploration
# =============================================================================
# df.head
# df.columns
# df[["total_hours", "discipline_code"]].groupby(["discipline_code"]).sum()
# =============================================================================

# Data transformation
df["period"] = df["period"].astype(str)
df["total_hours"] = df["total_hours"].astype(float)
df["client_suffix"] = df["client_suffix"].astype(str).str.zfill(2)
df["project_code"] = df["client_code"]+"-"+df["client_suffix"]
df.sort_values(by=['period'], inplace = True)

# building components
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO],
           meta_tags=[
               {   # check if device is a mobile device. This is a must if you do any mobile styling
                'name': 'viewport',
                'content': 'width=device-width, initial-scale=1'
                }
                   ]
           ) 
cons_dropdown = dcc.Dropdown(options=df["name_fam_last_first"].unique(),
                            value='Lim, Ken',  # initial value displayed when page first loads
                             clearable=False)
display_dropdown = dcc.Dropdown(options=['Aggregate', 'Detailed'],
                                value = 'Aggregate',
                                clearable=False)
m_graph = dcc.Graph(figure={}) # by month
p_graph = dcc.Graph(figure={}) # by project

# Customize your own Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([cons_dropdown], width=8, align = 'left'),
        dbc.Col([display_dropdown], width = 3, align = 'right')
    ]),
    dbc.Row([
        dbc.Col([m_graph])
    ]),
    dbc.Row([
        dbc.Col([p_graph])
    ])
])

# Callback allows components to interact
@app.callback(
    Output(m_graph, 'figure'),
    Output(p_graph, 'figure'),
    Input(cons_dropdown, 'value'),
    Input(display_dropdown, 'value')
)
def update_graph(cons_name, disp_level):  # function arguments come from the component property of the Input
    
    if disp_level == 'Aggregate':

        fig1 = px.histogram(data_frame=df[df['name_fam_last_first']==cons_name], 
                           x='period', 
                           y='total_hours', 
                           labels={'total_hours': 'Billable Hours'},
                           height = 750)
        
        # to allow for hover_name and hover_data
        df2=df[df['name_fam_last_first']==cons_name].groupby('project_code', as_index=False).agg(total_hours=("total_hours", "sum"),
                                                                                 name=('name', set),
                                                                                 description=('description', set))
        df2['name'] = df2.name.apply(lambda x: x.pop())
        df2['description'] = df2.description.apply(lambda x: x.pop())
        
        fig2 = px.bar(data_frame=df2,
                      x = 'total_hours',
                      y = 'project_code',
                      labels={'total_hours': 'Billable Hours'},
                      hover_name= 'name',
                      hover_data= ['description'],
                      height = 750)
        
    else:    
        fig1 = px.bar(data_frame=df[df['name_fam_last_first']==cons_name],
                     x='period', 
                     y='total_hours', 
                     color = 'project_code',
                     labels={'total_hours': 'Billable Hours'},
                     height = 900)
    
        fig2 = px.bar(data_frame=df[df['name_fam_last_first']==cons_name],
                      x = 'total_hours',
                      y = 'project_code',
                      color = 'period',
                      labels={'total_hours': 'Billable Hours'},
                      hover_name = 'name',
                      hover_data= ['description'],
                      height = 900)
    
    fig1.update_xaxes(categoryorder='category ascending')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis = {'categoryorder':'category ascending'})
    
    return fig1, fig2 # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8062)
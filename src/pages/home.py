# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:42:11 2022

@author: rongx
"""
import base64
import io

from dash import callback, register_page
from dash_extensions.enrich import Output, Input, State, ServersideOutput, html, dcc, Trigger  # pip install dash-extensions
import dash_bootstrap_components as dbc

import pandas as pd

register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

layout = dbc.Container([]) # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
#     dbc.Row([
#         dbc.Col([
#             dcc.Upload(
#                 id='upload-data',
#                 children=html.Div([
#                     'Drag and Drop or ',
#                     html.A('Select Files')
#                 ]),
#                 style={
#                     'width': '100%',
#                     'height': '60px',
#                     'lineHeight': '60px',
#                     'borderWidth': '1px',
#                     'borderStyle': 'dashed',
#                     'borderRadius': '5px',
#                     'textAlign': 'center',
#                     'margin': '10px'
#                 },
#                 multiple=False)
#         ])
#     ]),
#     dbc.Row([
#         html.Div([
#             dbc.Card(children="", id= "f_name", body = True)
#         ]),        
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dbc.Button("Upload", id="btn", color="info", class_name= "border rounded", type = "submit")
#         ],
#         className="d-grid gap-2 d-md-fkex justify-content-md-end")
#     ]),
#     dbc.Row([
#         html.Div([
#             dbc.Card(children="", id= "status", body = True)
#         ]),        
#     ]),
#     dcc.Store(id="store", data=[], storage_type='memory')
# ], id = "upload_component")

# def parse_contents(contents, filename):
#     content_type, content_string = contents.split(',')

#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
    
#     # Data transformation
#     df["period"] = df["period"].astype(str)
#     df["total_hours"] = df["total_hours"].astype(float)
#     df["client_suffix"] = df["client_suffix"].astype(str).str.zfill(2)
#     df["project_code"] = df["client_code"]+"-"+df["client_suffix"]
#     df.sort_values(by=['period'], inplace = True)
    
#     return df

# @callback(Output("f_name", "children"),
#           Input("upload-data", "contents"),
#           State("upload-data", "filename"))
# def select_data(content, filename):
#     return filename


# @callback(ServersideOutput("store", "data"),
#               Output("status", "children"),
#               Trigger("btn", "n_clicks"),
#               State("upload-data", "contents"),
#               State("upload-data", "filename"),
#               prevent_initial_call=True)
# def upload_data(n_clicks, content, filename):
#     ddf = parse_contents(content, filename)
#     return ddf.to_dict('records'), "Success!"


    
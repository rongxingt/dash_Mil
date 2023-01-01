# notes
'''
This file is for housing the main dash application.
This is where we define the various css items to fetch as well as the layout of our application.
'''

# package imports
import base64
import io

from dash_extensions.enrich import Dash, html, dcc, Output, Input, page_container, State
import dash_bootstrap_components as dbc
import pandas as pd

# local imports
from components import navbar

app = Dash(
    __name__,
    use_pages=True,    # turn on Dash pages
    meta_tags=[
        {   # check if device is a mobile device. This is a must if you do any mobile styling
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        }
    ],
    suppress_callback_exceptions=True,
    title='Dash app structure',
)



def serve_layout():
    '''Define the layout of the application'''
    return html.Div(
        [
            navbar,
            dbc.Container([ # this code section taken from Dash docs https://dash.plotly.com/dash-core-components/upload
               dbc.Row([
                   dbc.Col([
                       dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            multiple=False)
                    ])
                ]),
                dbc.Row([
                    html.Div([
                        dbc.Card(children="", id= "f_name", body = True)
                    ]),        
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Upload", id="btn", color="info", class_name= "border rounded", type = "submit")
                    ],
                    className="d-grid gap-2 d-md-fkex justify-content-md-end")
                ]),
                dcc.Loading(dcc.Store(id="store"), fullscreen=True, type="dot")
            ], id = "upload_component"),
            dbc.Container(
                page_container,
                class_name='my-2'
            ),
        ]
    )

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    # Data transformation
    df["period"] = df["period"].astype(str)
    df["total_hours"] = df["total_hours"].astype(float)
    df["client_suffix"] = df["client_suffix"].astype(str).str.zfill(2)
    df["project_code"] = df["client_code"]+"-"+df["client_suffix"]
    df.sort_values(by=['period'], inplace = True)
    
    return df

@app.callback(Output("f_name", "children"),
          Input("upload-data", "contents"),
          State("upload-data", "filename"),
)
def select_data(content, filename):
    return filename


@app.callback(Output("store", "data"),
              Output("upload_component", "style"),
              Input("btn", "n_clicks"),
              State("upload-data", "contents"),
              State("upload-data", "filename"),
              prevent_initial_call=True)
def upload_data(n_clicks, content, filename):
    ddf = parse_contents(content, filename)
    return ddf.to_dict('records'), {'display': 'none'}


              
app.layout = serve_layout   # set the layout to the serve_layout function
server = app.server         # the server is needed to deploy the application

if __name__ == "__main__":
    app.run_server(debug=True, port= 8062)


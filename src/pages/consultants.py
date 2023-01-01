# package imports

import dash
from dash_extensions.enrich import dcc, callback, Output, Input, State, html
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
import pandas as pd                        # pip install pandas


# import the required file 
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../dataset/Time_client code and consultant hours list - Jan-Jun'22.xlsx").resolve()
# df = pd.read_excel(DATA_PATH)

# Data exploration
# =============================================================================
# df.head
# df.columns
# df[["total_hours", "discipline_code"]].groupby(["discipline_code"]).sum()
# =============================================================================

# Data transformation
# df["period"] = df["period"].astype(str)
# df["total_hours"] = df["total_hours"].astype(float)
# df["client_suffix"] = df["client_suffix"].astype(str).str.zfill(2)
# df["project_code"] = df["client_code"]+"-"+df["client_suffix"]
# df.sort_values(by=['period'], inplace = True)


dash.register_page(
    __name__,
    path='/consultants',
)

display_dropdown = dcc.Dropdown(id = "display_dropdown",
                                options=['Aggregate', 'Detailed'],
                                value = 'Aggregate',
                                clearable=False,
                                persistence=True,
                                persistence_type='session')
m_graph = dcc.Graph(figure={}) # by month
p_graph = dcc.Graph(figure={}) # by project

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(id="cons_container", children=[]), width=8),
        dbc.Col([display_dropdown], width = 3)
    ]),
    dbc.Row([
        dbc.Col([m_graph])
    ]),
    dbc.Row([
        dbc.Col([p_graph])
    ])
], id = "consultant_component", style = {'display': 'none'})

@callback(
    Output('cons_container', 'children'),
    Output('consultant_component', 'style'),
    Input('store', 'data')
)
def init_graph(data):
    if data is None:
        return [[], {'display': 'none'}]
    
    df = pd.DataFrame(data)
    cons_name = df['name_fam_last_first'].unique()
    print(cons_name)
    return [dcc.Dropdown(id='cons_dropdown',
                        options= cons_name,
                        value=cons_name[0],  # initial value displayed when page first loads
                        clearable=False,
                        persistence=True,
                        persistence_type='session'),
            {'display': 'block'}]

#Callback allows components to interact
@callback(
    Output(m_graph, 'figure'),
    Output(p_graph, 'figure'),
    Input('cons_dropdown', 'value'),
    Input(display_dropdown, 'value'),
    State('store', 'data'),
    prevent_initial_call = True
)
def update_graph(cons_name, disp_level, data):  # function arguments come from the component property of the Input    
    df = pd.DataFrame(data)
    if cons_name is None:
        return {}, {}
        
    elif disp_level == 'Aggregate':

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
    
    
    
    return fig1, fig2# returned objects are assigned to the component property of the Output

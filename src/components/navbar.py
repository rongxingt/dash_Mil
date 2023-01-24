# notes
'''
This file is for creating a navigation bar that will sit at the top of your application.
Much of this page is pulled directly from the Dash Bootstrap Components documentation linked below:
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
'''

# package imports
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

# local imports
from utils.images import logo_encoded

# component
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                'Home',
                                href='/'
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                'Consultants',
                                href='/consultants'
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                'Project',
                                href='/project'
                            )
                        ),
                    ]
                ),
                id='navbar-collapse',
                navbar=True
            ),
            html.A(
                dbc.Row(
                    [   
                        dbc.Col(html.Img(src=logo_encoded, height='50px')),
                    ],
                    align='center',
                    className='float-end',
                ),
                href='https://www.my-milliman.com/en-gb/',
                style={'textDecoration': 'none'},
            )
        ]
    ),
    color="primary",
    dark = True
)

# add callback for toggling the collapse on small screens
@callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open'),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

from re import X
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests, base64
from io import BytesIO
import dash_core_components as dcc
import plotly.graph_objects as go
from collections import Counter
import pandas as pd
import openpyxl
import plotly.express as px


#data collection for graphs
excel1 = 'QC Process Tracker 2021.xlsx'

df_home1 = pd.read_excel(r'C:\Users\dsouzsa4\Novartis Pharma AG\Submission Quality - QC\Hyderabad Team\Vendor Management\QC Process Tracker 2021.xlsx', header = 10,)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
tcs = df_home1.loc[(df_home1["Vendor/\nNVS QC"]=='TCS')| (df_home1["Vendor/\nNVS QC"]== 'CACTUS') | (df_home1["Vendor/\nNVS QC"]== 'NVS'), ['Document\nType']]
count = tcs["Document\nType"].value_counts()
tcsgant = df_home1.loc[(df_home1["Vendor/\nNVS QC"]=='TCS')| (df_home1["Vendor/\nNVS QC"]== 'CACTUS'), ['Project\nCode','QC Start Date\nActual', 'QC End Date\nActual *','Vendor/\nNVS QC' ]]



#Navbar
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

dropdown = dbc.DropdownMenu(children=[
    dbc.DropdownMenuItem('Vendor Tracker', href='https://www.youtube.com/watch?v=P-XYio7G_Dg'),
    dbc.DropdownMenuItem('Hyd Calendar', href='https://www.geeksforgeeks.org/working-with-pdf-files-in-python/')

],
nav=True,
in_navbar=True,
label='Important Links'

)

navbar = dbc.Navbar(
    dbc.Container(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("QC Dashboard", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(dbc.Nav([dropdown], className='ml-auto',navbar=True), id="navbar-collapse", navbar=True),
    ],
    ),

    color="dark",
    dark=True,
    className='mb-5'
)

#Side bar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 63,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("QC Metrics", className="display-4"),
        html.Hr(),
        html.P(
            "Click on the pages to see different graph", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Gannt Chart", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
#Appcomponents


app.layout = html.Div(
    [dcc.Location(id ='url'), navbar, sidebar, content])



#App callbacks
# Navbar
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#sidebar callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1('Doc type wise distribution-2021',
                style={'textAlign': 'center'} ),

            dcc.Graph(id='piechart',
            figure=px.pie(count, values=count.values, names= count.index))
        ]
    elif pathname == "/page-1":
        return [
            html.H1('Vendor Projects Timeline-2021',
                style={'textAlign': 'center'} ),

            dcc.Graph(id='Ganntchart',
            figure=px.timeline(tcsgant, x_start = 'QC Start Date\nActual', x_end= 'QC End Date\nActual *', y = "Project\nCode", color='Vendor/\nNVS QC' )
            )
        ]
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)

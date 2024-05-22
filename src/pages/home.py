import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from helpers import avg_prices_map_fig, update_bar_plot
from config import app_config

dash.register_page(__name__, path='/')


layout = dbc.Container(
    [
        dbc.Row(
    [
        dbc.Col(
            html.Div("Select region:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': region, 'value': region}
                    for region in app_config['regions']
                ],
                value='South East',  # Default selected region
            ),
            width=2
        ),
        dbc.Col(
            html.Div("Select month:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='month-dropdown',
                options=[{"label": i, "value": i} for i in app_config['months']],
                value='1',  # Default selected year
            ),
            width=2,
        ),
    ],
    className = "dropdown-row"
),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='avg-price-map',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

#define callbacks

@callback(
    Output('avg-price-map', 'figure'),
     [Input('region-dropdown', 'value'),
      Input('month-dropdown', 'value')]
)
def update_plot(selected_region, selected_month):
    return avg_prices_map_fig(selected_region, selected_month)


@callback(
    Output('bar-plot', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_bar_plot_callback(selected_region, selected_month):
    return update_bar_plot(selected_region, selected_month)

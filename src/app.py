import dash
from dash import html
import dash_bootstrap_components as dbc


# Create the dash app
app = dash.Dash(__name__,  use_pages=True, external_stylesheets=[dbc.themes.SLATE, '/assets/custom.css'])

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Prices by month in 2023", href="/")),
        dbc.NavItem(dbc.NavLink("Volume", href="/volume")),
    ],
    brand="Property Prices trends in the UK - Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Meeran Muhammad Tabish | GitHub", href="https://github.com/thetabish/dash_project"), align="right"),
            dbc.Col(html.P("Please wait for the graphs to show up, it could take a few minutes."), align="left")
        ],
    ),
    className="footer",
    fluid=True,
)

# Overall layout
app.layout = html.Div([
    navbar,  # Include the navigation bar
    dash.page_container,
    footer
])

server = app.server

# Run the dash app
if __name__ == '__main__':
    app.run_server(debug=False)

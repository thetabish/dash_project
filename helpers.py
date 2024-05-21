import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import geopandas as gpd
import plotly.express as px
import pandas as pd
import numpy as np
import calendar
from config import app_config
import plotly.graph_objs as go
import json

# Define the GeoJSON data globally
geojson_data = None
current_selected_region = None



def avg_prices_map_fig(selected_region, selected_month):
    csv_file_path = f'processed_data/average_price_by_month/region_data_{selected_month}.csv'
    data = pd.read_csv(csv_file_path)

    data = data[data['region'] ==selected_region]

    region_geojson_path = f'geo_json/regions/{selected_region}_postcode_sectors.geojson'
    region_geojson = gpd.read_file(region_geojson_path)
    key_min = np.percentile(data.avg_price, 5)
    key_max = np.percentile(data.avg_price, 95)
    region_config = app_config['regions'][selected_region]
    selected_month = int(selected_month)
    month_name = calendar.month_name[selected_month]
    

    fig = px.choropleth_mapbox(
        data,
        geojson=region_geojson,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='avg_price',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center= region_config['center'],
        zoom = region_config['zoom'],
        opacity=0.5,
        labels={'avg_price':'Average Price £'},
        title=f'Average price by postcode sector for {selected_region} in {month_name}',
        hover_data = {'volume':True},
        range_color = [key_min, key_max]
    )
    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Legend Title'), orientation='h', x=1, y=1.02),
    )
    return fig

def update_bar_plot(selected_region,selected_month):
    # Load the preprocessed CSV containing average prices and volumes
    csv_file_path = 'processed_data/region_avg_price/region_avg_prices.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data for the selected region
    data = data[data['region'] == selected_region]

    # Aggregate volume by year
    aggregated_data = data.groupby('month')['volume'].sum().reset_index()
    selected_month = int(selected_month)
    month_name = calendar.month_name[selected_month]

    # Create stacked bar plot
    fig = px.bar(
        data,
        x='month',
        y='avg_price',
        color='property_type',
        title=f'Average price and sales volume for {selected_region} in {month_name}',
        barmode='stack',  # Set the barmode to 'stack' for stacked bars
    )

    # Add a line plot for the aggregated volume
    fig.add_trace(
        go.Scatter(x=aggregated_data['month'], y=aggregated_data['volume'], name='Volume', yaxis='y2', mode='lines+markers')
    )

    # Update legend names
    legend_names = {'D': 'Detached', 'S': 'Semi-Detached', 'T': 'Terraced', 'F': 'Flat'}
    fig.for_each_trace(lambda t: t.update(name=legend_names.get(t.name, t.name)))

    # Update layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Average Price £',
        yaxis2=dict(title='Volume',overlaying='y',showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def read_geojson(selected_region):
    global geojson_data
    global current_selected_region

    if current_selected_region != selected_region or geojson_data is None:
        geojson_file_path = f'geo_json/regions/{selected_region}_postcode_sectors.geojson'
        with open(geojson_file_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)
        current_selected_region = selected_region

    return geojson_data

def update_volume_plot(selected_year, selected_region):
    # Load data
    csv_file_path = f'processed_data/volume_by_year/region_total_volume_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    fig = px.line(data,
                  x='month',
                  y='volume',
                  color='region',
                  markers=True,
                  title=f'Volume trend for all regions in {selected_year} by month')
    
    # Update layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Volume',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_volume_map(selected_year, selected_region):
    # Load the CSV file based on the selected year
    csv_file_path = f'processed_data/average_price_by_year/region_data_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    key_min = np.percentile(data.volume, 1)
    key_max = np.percentile(data.volume, 99)

    # Create choropleth map
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='volume',
        color_continuous_scale='Viridis',
        range_color= [key_min,key_max],
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'volume': 'Volume'},
        title=f'Volume by postcode sector for {selected_region} in {selected_year}',
        hover_data={'volume': True},
    )

    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

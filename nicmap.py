import dash
from dash import dcc
from dash import html
import pandas as pd
import geopandas as gpd
import plotly.express as px

# 1. Initialize the Dash app
app = dash.Dash(__name__)

# --- Geospatial Data Setup ---
# NOTE: You must ensure the 'shape_nicaragua/Nic2/NIC_adm2.shp' file
# is available in the correct path relative to this script.
try:
    # Load the shapefile for Nicaragua administrative level 2 (departments)
    departamento = gpd.read_file(r'shape_nicaragua/Nic2/NIC_adm2.shp')

    # Optional: Prepare a dummy data column for the map's color/hover information
    # to demonstrate interactivity. Assuming 'NAME_1' is the department name.
    # We create a random value for demonstration purposes.
    departamento['Value'] = [i % 5 for i in range(len(departamento))]

    # Create the Plotly figure from the GeoDataFrame
    # 'NAME_1' is used for the color and hover text, making the map dynamic
    fig = px.choropleth_mapbox(
        departamento,
        geojson=departamento.geometry,
        locations=departamento.index,
        color="Value",  # Column to determine color intensity
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",  # Light map style
        zoom=5.5,
        center={"lat": 12.8, "lon": -85.0},  # Centered roughly on Nicaragua
        opacity=0.7,
        hover_name="NAME_1",  # Show the department name on hover
        title="Interactive Map of Nicaragua Departments"
    )

    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

except Exception as e:
    # Handle error if the shapefile is not found or loaded correctly
    print(f"Error loading GeoDataFrame: {e}")
    departamento = None
    fig = {}
    map_error_message = f"Error loading map data: Please check the path to your shapefile ('shape_nicaragua/Nic2/NIC_adm2.shp'). Error: {e}"

# --- Layout Definition ---
app.layout = html.Div(children=[
    # Header
    html.H1(
        children='🌎 Nicaragua Department Visualization',
        style={
            'textAlign': 'center',
            'color': '#2ECC40'
        }
    ),

    # Map visualization component
    dcc.Graph(
        id='nicaragua-map',
        figure=fig,
        style={'height': '80vh'}  # Make the map a good size
    ),

    # Display error message if the GeoDataFrame failed to load
    html.Div(
        children=map_error_message if departamento is None else None,
        style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}
    )
])

# --- Callbacks (Removed interactivity since the dropdown is gone) ---
# Note: Since the map is static in this simplified example,
# the previous callback has been removed.

# 4. Run the app
if __name__ == '__main__':
    # Set a lower debug setting if you have issues running on certain environments
    app.run(debug=True)
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
import numpy as np

# Load the data
population = pd.read_csv('data/population.csv')

# plot each country on the map with the color representing the population
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]

# Merge the population data with the world data by country code
world = world.merge(population, how='left', left_on='iso_a3', right_on='Country Code')

for year in range(1960, 2024):
    #world['log_' + str(year)] = world[str(year)].apply(lambda x: round(np.log(x), 2) if x > 0 else 0)
    
    # population relative to 1960
    world['relative_1960_' + str(year)] = world[str(year)]/ world[str(1960)]
    
    # population relative to previous year
    if year > 1960:
        world['relative_previous_' + str(year)] = world[str(year)]/ world[str(year - 1)]


############################################################################################################

# population relative to 1960 plot


# get the maximum value of the relative population for any year
max_relative = min(5, world[[col for col in world.columns if 'relative_1960' in col]].max().max())

# Create the initial plot
fig = px.choropleth(data_frame=world, locations="iso_a3", color="relative_1960_2023",
                    hover_name="name", projection="natural earth",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    labels={'color': 'Population by Country'},
                    range_color=(1, max_relative),
                    #template='plotly_dark'
                    )

#Add a slider to select the year
years = [str(year) for year in range(1960, 2023)]
sliders = [dict(
    active=62,
    currentvalue={"prefix": "Year: "},
    pad={"t": 50},
    steps=[dict(label=year, method="update", args=[{"z": [world['relative_1960_' + year]]}]) for year in years]
)]


fig.update_layout(sliders=sliders)

# Update function for the checkbox
def update(year, mode):
    logging.info(f"Updating the plot for year {year} with mode {mode}")
    
    fig.update_traces(z=world['relative_1960_' + year], 
                        zmin=1, 
                        zmax=max_relative, 
                        colorscale=px.colors.sequential.Plasma, 
                        colorbar=dict(title="Population relative to 1960", tickvals=[1, 2, 3, 4, 5], ticktext=["1x", "2x", "3x", "4x", "5x"]), 
                        range_color=(1, max_relative))

# save figure as html
fig.write_html("population_relative_1960.html")



############################################################################################################

# population relative to previous year plot

# get the maximum value of the relative population for any year
max_relative = min(1.05, world[[col for col in world.columns if 'relative_previous' in col]].max().max())
min_relative = max(0.95, world[[col for col in world.columns if 'relative_previous' in col]].min().min())

# Create the initial plot
fig = px.choropleth(data_frame=world, locations="iso_a3", color="relative_previous_2023",
                    hover_name="name", projection="natural earth",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    labels={'color': 'Population by Country'},
                    range_color=(min_relative, max_relative),
                    #template='plotly_dark'
                    )

#Add a slider to select the year
years = [str(year) for year in range(1961, 2023)]
sliders = [dict(
    active=62,
    currentvalue={"prefix": "Year: "},
    pad={"t": 50},
    steps=[dict(label=year, method="update", args=[{"z": [world['relative_previous_' + year]]}]) for year in years]
)]


fig.update_layout(sliders=sliders)

# Update function for the checkbox
def update(year, mode):
    logging.info(f"Updating the plot for year {year} with mode {mode}")
    
    fig.update_traces(z=world['relative_previous_' + year], 
                        zmin=1, 
                        zmax=max_relative, 
                        colorscale=px.colors.sequential.Plasma, 
                        colorbar=dict(title="Population relative to previous year"), 
                        range_color=(min_relative, max_relative))

# save figure as html
fig.write_html("population_relative_previous.html")
fig.show()
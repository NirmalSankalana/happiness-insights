import streamlit as st
import pandas as pd
import geopandas as gpd

GEOJSON_FILE = "data/countries.geo.json"
DATA_FILE = "data/data.csv"
REGIONS_FILE = "data/regions.csv"


@st.cache_resource
def load_data():
    geo_data = gpd.read_file(GEOJSON_FILE)
    data = pd.read_csv(DATA_FILE)
    regions = list(pd.read_csv(REGIONS_FILE)['Regions'])
    return geo_data, data, regions
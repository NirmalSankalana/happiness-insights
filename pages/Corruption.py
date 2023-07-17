import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import folium
import geopandas as gpd

APP_TITLE = "World Happiness Data"

DATA_FILE = "./data/data.csv"

@st.cache_resource
def load_data():
    data = pd.read_csv(DATA_FILE)
    return data
@st.cache_data
def filter_data(df, year):
    return df[df['Year'] == year]

def main():
    pass

if __name__ == "__main__":
    main()

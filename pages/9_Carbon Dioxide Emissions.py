import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium
import altair as alt

from services.load_data_service import load_data
from services.set_scale_service import get_scale
from services.filter_data_service import filter_data

# Charts
from graphs.line_chart import display_past_data
from graphs.scatter_plot import scatterplot

APP_TITLE = "Carbon dioxide emissions per capita (production) (tonnes)"

@st.cache_resource(experimental_allow_widgets=True)
def display_map(year, region, start, end, _geo_data, data):
    df = filter_data(data, year, region, start, end, 'Carbon dioxide emissions per capita (production) (tonnes)')
    if df.empty:
        st.warning("No data available for the selected filters.")
        return [], [], []
    
    myscale = get_scale(df, 'Carbon dioxide emissions per capita (production) (tonnes)')
    map = display_base_map(_geo_data, df, myscale)
    st_map = st_folium(map, width=700, height=450)

    # Manual country selection using multiselect
    countries = st.multiselect('Select Countries', df['Country'].unique().tolist(), default=[df["Country"].iloc[0]])

    # Filter data for the selected countries
    selected_data = df[df['Country'].isin(countries)]
    cde_rank = selected_data['Carbon dioxide emissions per capita (production) (tonnes) Rank'].tolist()
    cde_score = selected_data['Carbon dioxide emissions per capita (production) (tonnes)'].tolist()

    return countries, cde_rank, cde_score

@st.cache_resource(hash_funcs={folium.Map: lambda _: None})
def display_base_map(_geo_data, df, myscale):
    x_map = 17.51
    y_map = 22
    map = folium.Map(location=[x_map, y_map],
                     zoom_start=1, tiles=None, scrollWheelZoom=False)
    folium.TileLayer('CartoDB positron', name="Light Map",
                     control=False).add_to(map)

    choropleth = folium.Choropleth(
        geo_data=_geo_data,
        name='Choropleth',
        data=df,
        columns=['Country', 'Carbon dioxide emissions per capita (production) (tonnes)'],
        key_on="feature.properties.name",
        fill_color='PuBu',
        threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='Carbon dioxide emissions per capita (production) (tonnes)',
        smooth_factor=0
    ).add_to(map)

    def style_function(x): return {'fillColor': '#ffffff',
                                   'color': '#000000',
                                   'fillOpacity': 0.1,
                                   'weight': 0.1}

    def highlight_function(x): return {'fillColor': '#000000',
                                       'color': '#000000',
                                       'fillOpacity': 0.50,
                                       'weight': 0.1}

    df_indexed = df.set_index('Country')
    for feature in choropleth.geojson.data['features']:
        country = feature["properties"]['name']
        feature['properties']['cde_score'] =round(df_indexed.loc[country,
                                                                  'Carbon dioxide emissions per capita (production) (tonnes)'],2) if country in list(df_indexed.index) else 'N/A'
        feature['properties']['cde_rank'] = int(
            df_indexed.loc[country, 'Carbon dioxide emissions per capita (production) (tonnes) Rank']) if country in list(df_indexed.index) else 'N/A'

    NIL = folium.features.GeoJson(
        choropleth.geojson.data,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'cde_score', 'cde_rank'],
            aliases=['Country: ', 'Carbon dioxide emissions per capita (production) (tonnes) Rank', 'Carbon dioxide emissions per capita (production) (tonnes)'],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    map.add_child(NIL)
    map.keep_in_front(NIL)
    return map


def main():
    st.title(APP_TITLE)
    geo_data, data, regions = load_data()
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox('Year', (2021, 2020, 2019, 2018, 2017, 2016, 2015))
    with col2:
        region = st.selectbox('Region', regions)
    with col3:
        start, end = st.select_slider('Range',
                                      options=pd.Series(list(range(0, 50, 5))),
                                      value=(0, 45))
    scatterplot(data, year, region, start, end, 'Carbon dioxide emissions per capita (production) (tonnes)', 'Happiness Score')
    countries, happiness_ranks, happiness_scores = display_map(
        year, region, start, end, geo_data, data)

    if countries:
        display_past_data(data, countries, 'Year', 'Carbon dioxide emissions per capita (production) (tonnes)', 'Country', ['Country', 'Carbon dioxide emissions per capita (production) (tonnes)', 'Carbon dioxide emissions per capita (production) (tonnes) Rank'], 'Carbon dioxide emmission per capita from 2015 to 2021')

        display_past_data(data, countries, 'Year', 'Happiness Score', 'Country',
                              ['Country', 'Happiness Score', 'Happiness Rank'], 'Happiness Score from 2015 to 2021')


if __name__ == "__main__":
    main()

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

APP_TITLE = "Inequality in education"
select_country = list()


def display_map(year, region, start, end, _geo_data, data):
    df = filter_data(data, year, region, start, end, 'Inequality in eduation')
    if df.empty:
        st.warning("No data available for the selected filters.")
        return [], [], []

    myscale = get_scale(df, 'Inequality in eduation')
    map = display_base_map(_geo_data, df, myscale, region)
    st_map = st_folium(map, width=700, height=450)

    if st_map['last_active_drawing']:
        properties = st_map['last_active_drawing']['properties']
        country = properties.get('name')
        select_country.append(country)
    # Manual country selection using multiselect
    countries = st.multiselect('Select Countries', df['Country'].unique().tolist(), default=[df["Country"].iloc[0]])

    select_country.extend(countries)

    selected_data = df[df['Country'].isin(select_country)]
    iie_rank = selected_data['Inequality in eduation Rank'].tolist()
    iie_score = selected_data['Inequality in eduation'].tolist()

    return select_country, iie_rank, iie_score


@st.cache_resource(hash_funcs={folium.Map: lambda _: None})
def display_base_map(_geo_data, df, myscale, region=""):
    region_focus = {
        "": [17.51, 22],
        'Australia and New Zealand': [-28, 145],
        'Central Asia': [46, 60],
        'Eastern Asia': [33, 105],
        'Eastern Europe': [17.51, 22],
        'Latin America and the Caribbean': [3, -67],
        'Melanesia': [17, 22],
        'Micronesia': [17, 22],
        'Northern Africa': [31, 12],
        'Northern America': [51, -115],
        'Northern Europe': [66, 16],
        'Polynesia': [17, 22],
        'South-eastern Asia': [1.8, 114],
        'Southern Asia': [18, 77],
        'Southern Europe': [43, 10],
        'Sub-Saharan Africa': [1, 19],
        'Western Asia': [32, 39.6],
        'Western Europe': [48, 6]
    }
    region_zoom = {
        "": 1,
        'Australia and New Zealand': 2,
        'Central Asia': 3,
        'Eastern Asia': 2,
        'Eastern Europe': 2,
        'Latin America and the Caribbean': 2,
        'Melanesia': 2,
        'Micronesia': 2,
        'Northern Africa': 3,
        'Northern America': 2,
        'Northern Europe': 2,
        'Polynesia': 2,
        'South-eastern Asia': 3,
        'Southern Asia': 3,
        'Southern Europe': 4,
        'Sub-Saharan Africa': 3,
        'Western Asia': 3,
        'Western Europe': 3
    }
    # x_map = 17.51
    # y_map = 22
    # st.write(st.session_state)
    map = folium.Map(location=region_focus.get(region),
                     zoom_start=region_zoom.get(region), tiles=None, scrollWheelZoom=False)
    folium.TileLayer('CartoDB positron', name="Light Map",
                     control=False).add_to(map)

    choropleth = folium.Choropleth(
        geo_data=_geo_data,
        name='Choropleth',
        data=df,
        columns=['Country', 'Inequality in eduation'],
        key_on="feature.properties.name",
        fill_color='YlGnBu',
        threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='Inequality in eduation',
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
        feature['properties']['iie_score'] = round(df_indexed.loc[country,
        'Inequality in eduation'], 2) if country in list(df_indexed.index) else 'N/A'
        feature['properties']['iie_rank'] = int(
            df_indexed.loc[country, 'Inequality in eduation Rank']) if country in list(df_indexed.index) else 'N/A'

    NIL = folium.features.GeoJson(
        choropleth.geojson.data,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'iie_score', 'iie_rank'],
            aliases=['Country: ', 'Inequality in eduation Rank', 'Inequality in eduation'],
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
                                      options=pd.Series(list(range(0, 60, 5))),
                                      value=(0, 55))
    scatterplot(data, year, region, start, end, 'Inequality in eduation', 'Happiness Score')
    countries, happiness_ranks, happiness_scores = display_map(
        year, region, start, end, geo_data, data)

    if countries:
        display_past_data(data, countries, 'Year', 'Inequality in eduation', 'Country',
                          ['Country', 'Inequality in eduation', 'Inequality in eduation Rank'], 'Inequality in eduation from 2015 to 2021')

        display_past_data(data, countries, 'Year', 'Happiness Score', 'Country',
                          ['Country', 'Happiness Score', 'Happiness Rank'], "Happiness Score from 2015 to 2021")


if __name__ == "__main__":
    main()

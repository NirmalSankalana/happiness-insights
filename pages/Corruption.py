import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import folium
import geopandas as gpd
import altair as alt

APP_TITLE = "Corruption vs Happiness"
GEOJSON_FILE = "data/countries.geo.json"
DATA_FILE = "data/data.csv"


@st.cache_resource
def load_data():
    geo_data = gpd.read_file(GEOJSON_FILE)
    data = pd.read_csv(DATA_FILE)
    return geo_data, data


@st.cache_data
def get_scale(df):
    myscale = (df['Corruption'].quantile(
        (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))).tolist()
    return myscale


@st.cache_data
def filter_data(df, year, region, start, end):
    filtered_df = df.loc[(df['Year'] == year) &
                         (df['Corruption'] >= start) &
                         (df['Corruption'] <= end)]
    if region and region != "":
        filtered_df = filtered_df.loc[filtered_df['Region'] == region]
        
    return filtered_df


def display_map(year, region, start, end, _geo_data, data):
    df = filter_data(data, year, region, start, end)
    if df.empty:
        st.warning("No data available for the selected filters.")
        return "", "", ""
    
    myscale = get_scale(df)
    map = display_base_map(_geo_data, df, myscale)
    st_map = st_folium(map, width=700, height=450)
    country = ''
    happiness_rank = ''
    corruption = ''
    corruption_rank = ''
    if st_map['last_active_drawing']:
        properties = st_map['last_active_drawing']['properties']
        country = properties.get('name', '')
        corruption = properties.get('corruption', '')
        corruption_rank = properties.get('corruption_rank', '')
        happiness_rank = properties.get('happiness_rank', '')
    else:
        country = df["Country"].iloc[0]
        happiness_rank = df.loc[df["Country"] == country, "Happiness Rank"].iat[0]
        corruption_rank = df.loc[df["Country"] == country, "Corruption Rank"].iat[0]
        corruption = round(df.loc[df["Country"] == country, "Corruption"].iat[0],2)
    return country, corruption_rank, happiness_rank, corruption, 



@st.cache_resource
def display_past_data(df, country):
    df = df.loc[df["Country"] == country].copy()  # Create a copy of the DataFrame
    df['Year'] = df['Year'].astype(int)
    
    # Create a new column for scaled Corruption
    df['Scaled Corruption'] = df['Corruption'] * 10

    # Plot Happiness Score and scaled Corruption on separate y-axes
    chart = alt.layer(
        alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('Year:O', axis=alt.Axis(format='d', labelFlush=False)),
            y=alt.Y('Happiness Score', title='Happiness Score'),
            tooltip=['Year:O', 'Corruption', 'Corruption Rank', 'Happiness Rank']
        ),
        alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('Year:O', axis=alt.Axis(format='d', labelFlush=False)),
            y=alt.Y('Scaled Corruption', title='Corruption (scaled by 10)'),
        )
    ).properties(
        width=alt.Step(80)  # Adjust the width as needed
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False
    )

    st.altair_chart(chart, use_container_width=True)



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
        columns=['Country', 'Corruption'],
        key_on="feature.properties.name",
        fill_color='YlGnBu',
        threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='Corruption',
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
        feature['properties']['corruption'] =round(df_indexed.loc[country,
                                                                  'Corruption'],2) if country in list(df_indexed.index) else 'N/A'
        feature['properties']['corruption_rank'] = int(
            df_indexed.loc[country, 'Corruption Rank']) if country in list(df_indexed.index) else 'N/A'
        feature['properties']['happiness_rank'] = int(
            df_indexed.loc[country, 'Happiness Rank']) if country in list(df_indexed.index) else 'N/A'

    NIL = folium.features.GeoJson(
        choropleth.geojson.data,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'corruption_rank', 'happiness_rank', 'corruption'],
            aliases=['Country: ', 'Corruption Rank', 'Happiness Rank', 'Corruption'],
            style=(
                "background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    map.add_child(NIL)
    map.keep_in_front(NIL)
    return map


def main():
    st.title(APP_TITLE)
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox('Year', (2021, 2020, 2019, 2018, 2017, 2016, 2015))
    with col2:
        region = st.selectbox('Region', ("",
            'Australia and New Zealand',
                                         'Central Asia',
                                         'Eastern Asia',
                                         'Eastern Europe',
                                         'Latin America and the Caribbean',
                                         'Melanesia',
                                         'Micronesia',
                                         'Northern Africa',
                                         'Northern America',
                                         'Northern Europe',
                                         'Polynesia',
                                         'South-eastern Asia',
                                         'Southern Asia',
                                         'Southern Europe',
                                         'Sub-Saharan Africa',
                                         'Western Asia',
                                         'Western Europe'))
    with col3:
        start, end = st.select_slider('Range',
                                      options=(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1),
                                      value=(0, 1))

    geo_data, data = load_data()
    country, corruption_rank, happiness_rank, corruption = display_map(
        year, region, start, end, geo_data, data)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Selected Country: ", f"{country}")
    with col2:
        st.metric("Corruption Rank: ", f"{corruption_rank}")
    with col3:
        st.metric("Happiness Rank: ", f"{happiness_rank}")

    if country:
        display_past_data(data, country)


if __name__ == "__main__":
    main()

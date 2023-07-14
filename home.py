# # import streamlit as st
# # from streamlit_folium import st_folium
# # import pandas as pd
# # import folium
# # import geopandas as gpd

# # APP_TITLE = "World Happiness Data"
# # GEOJSON_FILE = "./data/countries.geojson"
# # DATA_FILE = "./data/data.csv"

# # @st.cache_resource
# # def load_data():
# #     geo_data = gpd.read_file(GEOJSON_FILE)
# #     data = pd.read_csv(DATA_FILE)
# #     return geo_data, data

# # @st.cache_data
# # def get_scale(df):
# #     myscale = (df['Happiness Score'].quantile((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))).tolist()
# #     return myscale

# # @st.cache_data
# # def filter_data(df, year):
# #     return df[df['Year'] == year]

# # @st.cache_resource
# # def display_base_map(_geo_data, df, myscale):
# #     x_map = 17.51
# #     y_map = 22
# #     map = folium.Map(location=[x_map, y_map], zoom_start=1, tiles=None)
# #     folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(map)

# #     choropleth = folium.Choropleth(
# #         geo_data=_geo_data,
# #         name='Choropleth',
# #         data=df,
# #         columns=['Country', 'Happiness Score'],
# #         key_on="feature.properties.ADMIN",
# #         fill_color='YlGnBu',
# #         threshold_scale=myscale,
# #         fill_opacity=1,
# #         line_opacity=0.2,
# #         legend_name='Happiness Score',
# #         smooth_factor=0
# #     ).add_to(map)

# #     style_function = lambda x: {'fillColor': '#ffffff',
# #                                 'color': '#000000',
# #                                 'fillOpacity': 0.1,
# #                                 'weight': 0.1}
# #     highlight_function = lambda x: {'fillColor': '#000000',
# #                                     'color': '#000000',
# #                                     'fillOpacity': 0.50,
# #                                     'weight': 0.1}

# #     df_indexed = df.set_index('Country')
# #     for feature in choropleth.geojson.data['features']:
# #         country = feature["properties"]['ADMIN']
# #         feature['properties']['happiness_score'] = df_indexed.loc[country, 'Happiness Score'] if country in list(df_indexed.index) else 'N/A'

# #     NIL = folium.features.GeoJson(
# #         choropleth.geojson.data,
# #         style_function=style_function,
# #         control=False,
# #         highlight_function=highlight_function,
# #         tooltip=folium.features.GeoJsonTooltip(
# #             fields=['ADMIN', 'happiness_score'],
# #             aliases=['Country: ', 'Happiness Score'],
# #             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
# #         )
# #     )
# #     map.add_child(NIL)
# #     map.keep_in_front(NIL)
# #     return map

# # def display_map(year, geo_data, data):
# #     df = filter_data(data, year)
# #     myscale = get_scale(df)
# #     map = display_base_map(geo_data, df, myscale)
# #     st_map = st_folium(map, width=700, height=450)
# #     country = ''
# #     if st_map['last_active_drawing']:
# #         country = st_map['last_active_drawing']['properties']['ADMIN']
# #     st.write(country)
# #     return country


# # def main():
# #     st.title(APP_TITLE)
# #     geo_data, data = load_data()
# #     display_map(2020, geo_data, data)
# #     st.write(data)

# # if __name__ == "__main__":
# #     main()


# import streamlit as st
# from streamlit_folium import st_folium
# import pandas as pd
# import folium
# import geopandas as gpd

# APP_TITLE = "World Happiness Data"
# GEOJSON_FILE = "./data/countries.geojson"
# DATA_FILE = "./data/data.csv"

# @st.cache_resource
# def load_data():
#     geo_data = gpd.read_file(GEOJSON_FILE)
#     data = pd.read_csv(DATA_FILE)
#     return geo_data, data

# @st.cache_data
# def get_scale(df):
#     myscale = (df['Happiness Score'].quantile((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))).tolist()
#     return myscale

# @st.cache_data
# def filter_data(df, year):
#     return df[df['Year'] == year]

# @st.cache_data(experimental_allow_widgets=True)
# def display_map(year, _geo_data, data):
#     df = filter_data(data, year)
#     myscale = get_scale(df)
#     map = display_base_map(_geo_data, df, myscale)
#     st_map = st_folium(map, width=700, height=450)
#     country = ''
#     if st_map['last_active_drawing']:
#         country = st_map['last_active_drawing']['properties']['ADMIN']
#     return country

# @st.cache_resource(hash_funcs={folium.Map: lambda _: None})
# def display_base_map(_geo_data, df, myscale):
#     x_map = 17.51
#     y_map = 22
#     map = folium.Map(location=[x_map, y_map], zoom_start=1, tiles=None)
#     folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(map)

#     choropleth = folium.Choropleth(
#         geo_data=_geo_data,
#         name='Choropleth',
#         data=df,
#         columns=['Country', 'Happiness Score'],
#         key_on="feature.properties.ADMIN",
#         fill_color='YlGnBu',
#         threshold_scale=myscale,
#         fill_opacity=1,
#         line_opacity=0.2,
#         legend_name='Happiness Score',
#         smooth_factor=0
#     ).add_to(map)

#     style_function = lambda x: {'fillColor': '#ffffff',
#                                 'color': '#000000',
#                                 'fillOpacity': 0.1,
#                                 'weight': 0.1}
#     highlight_function = lambda x: {'fillColor': '#000000',
#                                     'color': '#000000',
#                                     'fillOpacity': 0.50,
#                                     'weight': 0.1}

#     df_indexed = df.set_index('Country')
#     for feature in choropleth.geojson.data['features']:
#         country = feature["properties"]['ADMIN']
#         feature['properties']['happiness_score'] = df_indexed.loc[country, 'Happiness Score'] if country in list(df_indexed.index) else 'N/A'

#     NIL = folium.features.GeoJson(
#         choropleth.geojson.data,
#         style_function=style_function,
#         control=False,
#         highlight_function=highlight_function,
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=['ADMIN', 'happiness_score'],
#             aliases=['Country: ', 'Happiness Score'],
#             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
#         )
#     )
#     map.add_child(NIL)
#     map.keep_in_front(NIL)
#     return map

# def main():
#     st.title(APP_TITLE)
#     geo_data, data = load_data()
#     country = display_map(2020, geo_data, data)
#     st.write(country)
#     st.write(data)

# if __name__ == "__main__":
#     main()

# import streamlit as st
# from streamlit_folium import st_folium
# import pandas as pd
# import folium
# import geopandas as gpd

# APP_TITLE = "World Happiness Data"
# GEOJSON_FILE = "./data/countries.geojson"
# DATA_FILE = "./data/data.csv"

# @st.cache_resource
# def load_data():
#     geo_data = gpd.read_file(GEOJSON_FILE)
#     data = pd.read_csv(DATA_FILE)
#     return geo_data, data

# @st.cache_data
# def get_scale(df):
#     myscale = (df['Happiness Score'].quantile((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))).tolist()
#     return myscale

# @st.cache_data
# def filter_data(df, year):
#     return df[df['Year'] == year]

# @st.cache_resource
# def display_base_map(_geo_data, df, myscale):
#     x_map = 17.51
#     y_map = 22
#     map = folium.Map(location=[x_map, y_map], zoom_start=1, tiles=None)
#     folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(map)

#     choropleth = folium.Choropleth(
#         geo_data=_geo_data,
#         name='Choropleth',
#         data=df,
#         columns=['Country', 'Happiness Score'],
#         key_on="feature.properties.ADMIN",
#         fill_color='YlGnBu',
#         threshold_scale=myscale,
#         fill_opacity=1,
#         line_opacity=0.2,
#         legend_name='Happiness Score',
#         smooth_factor=0
#     ).add_to(map)

#     style_function = lambda x: {'fillColor': '#ffffff',
#                                 'color': '#000000',
#                                 'fillOpacity': 0.1,
#                                 'weight': 0.1}
#     highlight_function = lambda x: {'fillColor': '#000000',
#                                     'color': '#000000',
#                                     'fillOpacity': 0.50,
#                                     'weight': 0.1}

#     df_indexed = df.set_index('Country')
#     for feature in choropleth.geojson.data['features']:
#         country = feature["properties"]['ADMIN']
#         feature['properties']['happiness_score'] = df_indexed.loc[country, 'Happiness Score'] if country in list(df_indexed.index) else 'N/A'

#     NIL = folium.features.GeoJson(
#         choropleth.geojson.data,
#         style_function=style_function,
#         control=False,
#         highlight_function=highlight_function,
#         tooltip=folium.features.GeoJsonTooltip(
#             fields=['ADMIN', 'happiness_score'],
#             aliases=['Country: ', 'Happiness Score'],
#             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
#         )
#     )
#     map.add_child(NIL)
#     map.keep_in_front(NIL)
#     return map

# def display_map(year, geo_data, data):
#     df = filter_data(data, year)
#     myscale = get_scale(df)
#     map = display_base_map(geo_data, df, myscale)
#     st_map = st_folium(map, width=700, height=450)
#     country = ''
#     if st_map['last_active_drawing']:
#         country = st_map['last_active_drawing']['properties']['ADMIN']
#     st.write(country)
#     return country


# def main():
#     st.title(APP_TITLE)
#     geo_data, data = load_data()
#     display_map(2020, geo_data, data)
#     st.write(data)

# if __name__ == "__main__":
#     main()


import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import folium
import geopandas as gpd

APP_TITLE = "World Happiness Data"
GEOJSON_FILE = "./data/countries.geojson"
DATA_FILE = "./data/data.csv"

@st.cache_resource
def load_data():
    geo_data = gpd.read_file(GEOJSON_FILE)
    data = pd.read_csv(DATA_FILE)
    return geo_data, data

@st.cache_data
def get_scale(df):
    myscale = (df['Happiness Score'].quantile((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))).tolist()
    return myscale

@st.cache_data
def filter_data(df, year):
    return df[df['Year'] == year]

# @st.cache_data(experimental_allow_widgets=True)
def display_map(year, _geo_data, data):
    df = filter_data(data, year)
    myscale = get_scale(df)
    map = display_base_map(_geo_data, df, myscale)
    st_map = st_folium(map, width=700, height=450)
    country = ''
    happiness_score = ''
    if st_map['last_active_drawing']:
        properties = st_map['last_active_drawing']['properties']
        country = properties.get('ADMIN', '')
        happiness_score = properties.get('happiness_score', '')
    return country, happiness_score



@st.cache_resource(hash_funcs={folium.Map: lambda _: None})
def display_base_map(_geo_data, df, myscale):
    x_map = 17.51
    y_map = 22
    map = folium.Map(location=[x_map, y_map], zoom_start=1, tiles=None)
    folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(map)

    choropleth = folium.Choropleth(
        geo_data=_geo_data,
        name='Choropleth',
        data=df,
        columns=['Country', 'Happiness Score'],
        key_on="feature.properties.ADMIN",
        fill_color='YlGnBu',
        threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='Happiness Score',
        smooth_factor=0
    ).add_to(map)

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    df_indexed = df.set_index('Country')
    for feature in choropleth.geojson.data['features']:
        country = feature["properties"]['ADMIN']
        feature['properties']['happiness_score'] = df_indexed.loc[country, 'Happiness Score'] if country in list(df_indexed.index) else 'N/A'

    NIL = folium.features.GeoJson(
        choropleth.geojson.data,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['ADMIN', 'happiness_score'],
            aliases=['Country: ', 'Happiness Score'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    map.add_child(NIL)
    map.keep_in_front(NIL)
    return map

def main():
    st.title(APP_TITLE)
    geo_data, data = load_data()
    country, happiness_score = display_map(2020, geo_data, data)
    st.write(f"Selected Country: {country}")
    st.write(f"Happiness Score: {happiness_score}")
    st.write(data)



if __name__ == "__main__":
    main()

import streamlit as st

@st.cache_data
def filter_data(df, year, region, start, end, entity_name):
    filtered_df = df.loc[(df['Year'] == year) &
                         (df[entity_name] >= start) &
                         (df[entity_name] <= end)]
    if region and region != 'All':
        filtered_df = filtered_df.loc[filtered_df['Region'] == region]
        
    return filtered_df
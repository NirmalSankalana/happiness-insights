import streamlit as st

@st.cache_data
def get_scale(df, entity):
    myscale = (df[entity].quantile(
        (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))).tolist()
    return myscale
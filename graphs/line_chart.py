import streamlit as st
import altair as alt

@st.cache_resource
def display_line_chart(df, country, y_axis_name):
    df = df.loc[df["Country"] == country].copy()  # Create a copy of the DataFrame
    df['Year'] = df['Year'].astype(int)
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Year:O', axis=alt.Axis(format='d', labelFlush=False)),
        y=y_axis_name,
        tooltip=['Year:O', y_axis_name]
    ).properties(
        width=alt.Step(80)  # Adjust the width as needed
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False
    )
    
    st.altair_chart(chart, use_container_width=True)
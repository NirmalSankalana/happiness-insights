import streamlit as st
import altair as alt

from services.filter_data_service import filter_data

def scatterplot(data, year, region, start, end, x_axis, y_axis):
    var_rank = x_axis + " Rank"
    df = filter_data(data, year, region, start, end, x_axis)
    chart = alt.Chart(df).mark_point(
        opacity=0.7,
        size=80,  # Increased the size for better visibility
    ).encode(
        x=x_axis,
        y=y_axis,
        color='Region',  # Color the points by region
        tooltip=['Country', 'Happiness Rank', var_rank, x_axis, y_axis],  # Added tooltip information
    ).properties(
        width=alt.Step(80)  # Adjust the width as needed
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False,  # Show gridlines
        titleFontSize=14,  # Adjust the title font size
        labelFontSize=12,  # Adjust the label font size
    )

    st.altair_chart(chart, use_container_width=True)

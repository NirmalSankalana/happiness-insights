import streamlit as st
import altair as alt

import streamlit as st
import altair as alt

@st.cache_resource
def display_past_data(df, countries, x_axis, y_axis, color_channel, tooltip_data:list, title):
    df = df[df["Country"].isin(countries)].copy()  # Create a copy of the DataFrame
    df['Year'] = df['Year'].astype(int)
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(x_axis, axis=alt.Axis(format='d', labelFlush=False)),
        y=alt.Y(y_axis, axis=alt.Axis(title=y_axis)),  # Specify the title for y-axis
        color=color_channel,
        tooltip=tooltip_data
    ).properties(
        title=title,
        width=alt.Step(80)  # Adjust the width as needed
    ).configure_view(
        stroke=None
    ).configure_axis(
        grid=False,  # Show gridlines
        titleFontSize=14,  # Adjust the title font size
        labelFontSize=12,  # Adjust the label font size
    )
    
    st.altair_chart(chart, use_container_width=True)

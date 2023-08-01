import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from services.load_data_service import load_data

APP_TITLE = "Analysis"

def main():
    st.title(APP_TITLE)
    geo_data, data, regions = load_data()
    data = data.drop(columns=['Happiness Rank', 'Corruption Rank', 'Inequality in life expectancy'])
    data = data.iloc[:, 1: 13]
    # Calculate the correlation matrix
    correlation_matrix = data.corr()

    # Create a heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis',  # You can choose different color scales
    ))

    fig.update_layout(
        title='Realationship between happiness and its factors',
        xaxis_title='Features',
        yaxis_title='Features',
        width=800,  # Adjust the width as per your preference
        height=800,  # Adjust the height as per your preference
    )

    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

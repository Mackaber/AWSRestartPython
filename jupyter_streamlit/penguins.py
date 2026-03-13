import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🐧 Penguin Explorer")
df = pd.read_csv("penguins.csv")

# Create a native Streamlit sidebar widget
species = st.selectbox(
    "Select Species", ["Adelie", "Chinstrap", "Gentoo"]
)

# Filter and Plot (Same logic as Jupyter!)
filtered = df[df['species'] == species]
fig = px.scatter(filtered, x="flipper_length_mm", y="body_mass_g")

# Render in the web app
st.plotly_chart(fig)
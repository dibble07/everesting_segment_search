import folium
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Map Area Selector")

col1, col2 = st.columns([3, 1])

map = folium.Map(location=[51.476868, 0])

with col1:
    map_output = st_folium(map, width=1000)

with col2:
    st.write(map_output["bounds"])

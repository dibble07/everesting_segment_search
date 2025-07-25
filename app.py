import time

import folium
import streamlit as st
from streamlit_folium import st_folium

from strava import get_segment_overview

st.set_page_config(layout="wide")
st.title("Map Area Selector")

col1, col2 = st.columns([3, 2])

map = folium.Map(location=[51.476868, 0])

with col1:
    map_output = st_folium(map, use_container_width=True)

with col2:
    if (
        map_output["bounds"]["_southWest"]["lat"]
        and map_output["bounds"]["_northEast"]["lat"]
        and map_output["bounds"]["_southWest"]["lng"]
        and map_output["bounds"]["_northEast"]["lng"]
    ):
        time.sleep(0.5)
        df_segments = get_segment_overview(
            lat_lower=map_output["bounds"]["_southWest"]["lat"],
            lat_upper=map_output["bounds"]["_northEast"]["lat"],
            long_left=map_output["bounds"]["_southWest"]["lng"],
            long_right=map_output["bounds"]["_northEast"]["lng"],
        )
        st.dataframe(
            df_segments.sort_values(by="everesting_distance", ascending=True),
            use_container_width=True,
        )

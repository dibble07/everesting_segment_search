import time

import folium
import streamlit as st
from streamlit_folium import st_folium

from strava import get_segment_overview

# setup app
st.set_page_config(layout="wide")
st.title("Map Area Selector")

# initialise columns
col1, col2 = st.columns([1, 1])

# initialise map
map = folium.Map(location=[51.476868, 0])

# display map
with col1:
    map_output = st_folium(map, use_container_width=True)

# display segment stats from within map
with col2:
    if (
        map_output["bounds"]["_southWest"]["lat"]
        and map_output["bounds"]["_northEast"]["lat"]
        and map_output["bounds"]["_southWest"]["lng"]
        and map_output["bounds"]["_northEast"]["lng"]
    ):
        # delay api call if made too soon after previous one
        current_time = time.time()
        if "last_interaction" in st.session_state:
            delay = 2 - (current_time - st.session_state.last_interaction)
        else:
            delay = 0
        if delay > 0:
            time.sleep(delay)
            st.rerun()

        # get data for segments within map area
        df_segments = get_segment_overview(
            lat_lower=map_output["bounds"]["_southWest"]["lat"],
            lat_upper=map_output["bounds"]["_northEast"]["lat"],
            long_left=map_output["bounds"]["_southWest"]["lng"],
            long_right=map_output["bounds"]["_northEast"]["lng"],
        )
        st.session_state.last_interaction = current_time

        # display results
        st.dataframe(
            df_segments.sort_values(by="everesting_distance", ascending=True),
            use_container_width=True,
        )

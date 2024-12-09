import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Global Styles
st.set_page_config(layout="wide", page_title="Drone Search and Rescue Dashboard")

# Title
st.markdown("<h2 style='text-align: center;'>Drone Search and Rescue Dashboard</h2>", unsafe_allow_html=True)

# Page Layout
left, right = st.columns([3, 1])  # 75% (left) and 25% (right)

# Left Column (75%)
with left:
    # Row 1: Simulation Panel
    st.markdown("### Simulation Panel")
    uploaded_file = st.file_uploader("Upload a simulation file to view here.", type=["mp4", "avi"])
    if uploaded_file is not None:
        st.video(uploaded_file, format="mp4", start_time=0)

    # Row 2: Interactive Map and Path Planning
    st.markdown("---")
    col_map, col_path = st.columns(2)
    with col_map:
        st.markdown("### Interactive Map")
        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        m.add_basemap("OpenTopoMap")
        m.to_streamlit(height=300)
    with col_path:
        st.markdown("### Path Planning")
        st.empty()  # Placeholder for future implementation

    # Row 3: Buttons
    st.markdown("---")
    col_start, col_stop, col_wake_up, col_emergency = st.columns(4)

    with col_start:
        if st.button("Start"):
            st.write("Start button clicked!")

    with col_stop:
        if st.button("Stop"):
            st.write("Stop button clicked!")

    with col_wake_up:
        if st.button("Wake Up"):
            st.write("Wake Up button clicked!")

    with col_emergency:
        if st.button("Emergency Stop"):
            st.write("Emergency Stop button clicked!")

# Right Column (25%)
with right:
    # Drone Status Table
    st.markdown("### Drone Status")
    drone_data = [
        {"Drone ID": "Drone-1", "Battery (%)": 75, "Status": "Active"},
        {"Drone ID": "Drone-2", "Battery (%)": 90, "Status": "Active"},
        {"Drone ID": "Drone-3", "Battery (%)": 60, "Status": "Inactive"},
        {"Drone ID": "Drone-4", "Battery (%)": 50, "Status": "Active"},
        {"Drone ID": "Drone-5", "Battery (%)": 40, "Status": "Inactive"},
    ]
    df_drone = pd.DataFrame(drone_data)
    st.dataframe(df_drone, height=250)

    # People Found Table
    st.markdown("### People Found")
    people_data = [
        {"Name": "John", "Location": "Sector 1"},
        {"Name": "Anna", "Location": "Sector 2"},
        {"Name": "Tom", "Location": "Sector 3"},
        {"Name": "Kate", "Location": "Sector 4"},
        {"Name": "Emma", "Location": "Sector 5"},
    ]
    df_people = pd.DataFrame(people_data)
    st.dataframe(df_people, height=250)

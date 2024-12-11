import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Global Styles
st.set_page_config(layout="wide", page_title="Drone Search and Rescue Dashboard")

# Page Layout
left, right = st.columns([3, 1])  # 75% (left) and 25% (right)

# Left Column (75%)
with left:
    # ELEEVATE Header
    st.markdown("<h1 style='text-align: center;'>ELEEVATE</h1>", unsafe_allow_html=True)

    # Row 1: Simulation Panel - Two Boxes
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        uploaded_file1 = st.file_uploader("Upload Simulation 1", type=["mp4", "avi"])  # No title for file uploader
        if uploaded_file1 is not None:
            st.video(uploaded_file1, format="mp4", start_time=0)
    with col_sim2:
        uploaded_file2 = st.file_uploader("Upload Simulation 2", type=["mp4", "avi"])  # No title for file uploader
        if uploaded_file2 is not None:
            st.video(uploaded_file2, format="mp4", start_time=0)
    
    st.markdown("<hr style='margin-top: 3px; margin-bottom: 3px;'>", unsafe_allow_html=True)

    # Row 2: Interactive Map and Path Planning Placeholder
    col_map, col_path = st.columns(2)
    
    with col_map:
        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        m.add_basemap("OpenTopoMap")
        m.to_streamlit(height=250)
    
    with col_path:
        st.markdown(
            "<div style='height: 250px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center;'>"
            "<b>Path Planning Placeholder</b></div>",
            unsafe_allow_html=True,
        )

# Right Column (25%)
with right:
    # Drone Status Table
    drone_data = [
        {"Drone ID": "Drone-1", "Battery (%)": 75, "Status": "Active"},
        {"Drone ID": "Drone-2", "Battery (%)": 90, "Status": "Active"},
        {"Drone ID": "Drone-3", "Battery (%)": 60, "Status": "Inactive"},
        {"Drone ID": "Drone-4", "Battery (%)": 50, "Status": "Active"},
        {"Drone ID": "Drone-5", "Battery (%)": 40, "Status": "Inactive"},
    ]
    df_drone = pd.DataFrame(drone_data)
    st.dataframe(df_drone, height=220)

    st.markdown("<hr style='margin-top: 3px; margin-bottom: 3px;'>", unsafe_allow_html=True)

    # People Found Table and Compact Buttons
    col_table, col_buttons = st.columns([2, 1])
    
    with col_table:
        people_data = [
            {"Name": "John", "Location": "Sector 1"},
            {"Name": "Anna", "Location": "Sector 2"},
            {"Name": "Tom", "Location": "Sector 3"},
            {"Name": "Kate", "Location": "Sector 4"},
            {"Name": "Emma", "Location": "Sector 5"},
        ]
        df_people = pd.DataFrame(people_data)
        st.dataframe(df_people, height=220)

    with col_buttons:
        # Round Buttons (CSS Styling)
        button_styles = """
        <style>
        .round-button {
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background-color: #007BFF;
            color: white;
            width: 50px;
            height: 50px;
            margin: -8px auto; /* Reduced spacing between buttons */
            font-size: 14px;
            border: none;
            cursor: pointer;
        }
        .round-button:hover {
            background-color: #0056b3;
        }
        </style>
        """
        st.markdown(button_styles, unsafe_allow_html=True)

        # Adding Buttons Vertically with Less Margin
        st.markdown("<button class='round-button'>Start</button>", unsafe_allow_html=True)  # Start
        st.markdown("<button class='round-button'>Stop</button>", unsafe_allow_html=True)  # Stop
        st.markdown("<button class='round-button'>Wake</button>", unsafe_allow_html=True)  # Wake Up
        st.markdown("<button class='round-button'>E.S</button>", unsafe_allow_html=True)  # Emergency Stop

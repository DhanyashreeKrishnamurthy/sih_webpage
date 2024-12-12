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

    # Simulation Panel - Elongated Box for Simulation 1
    uploaded_file1 = st.file_uploader("Upload Simulation 1", type=["mp4", "avi"])  # No title for file uploader
    if uploaded_file1 is not None:
        st.video(uploaded_file1, format="mp4", start_time=0)

    st.markdown("<hr style='margin-top: 3px; margin-bottom: 3px;'>", unsafe_allow_html=True)

    # Row 2: Interactive Map and Path Planning Placeholder
    col_map, col_path = st.columns(2)
    
    # Interactive Map
    with col_map:
        options = list(leafmap.basemaps.keys())
        index = options.index("OpenTopoMap")
        basemap = st.selectbox("Select a basemap:", options, index)

        m = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        m.add_basemap(basemap)
        m.to_streamlit(height=250)
    
    # Path Planning Section with Heading
    with col_path:
        st.markdown("<h3 style='text-align: center;'>Path Planning</h3>", unsafe_allow_html=True)  # Add heading above the placeholder
        st.markdown(
            "<div style='height: 250px; background-color: #f0f0f0; display: flex; align-items: center; justify-content: center;'>"
            "<b>Path Planning Placeholder</b></div>",
            unsafe_allow_html=True,
        )

# Right Column (25%)
with right:
    # Drone Status Table with Buttons Beside Specific Drones
    drone_data = [
        {"Drone ID": "Drone-1", "(%)": 75, "Status": "Active"},
        {"Drone ID": "Drone-2", "(%)": 90, "Status": "Active"},
        {"Drone ID": "Drone-3", "(%)": 60, "Status": "Inactive"},
        {"Drone ID": "Drone-4", "(%)": 50, "Status": "Active"},
        {"Drone ID": "Drone-5", "(%)": 40, "Status": "Inactive"},
    ]
    df_drone = pd.DataFrame(drone_data)

    # Buttons next to Drone-1 and Drone-4
    col_buttons = st.columns([1, 1, 1])  # Three columns for buttons next to specific drones
    
    col_buttons[0].markdown("<button class='round-button return-button'>POV 1</button>", unsafe_allow_html=True)  # Drone-1
    col_buttons[2].markdown("<button class='round-button return-button'>POV 4</button>", unsafe_allow_html=True)  # Drone-4

    st.dataframe(df_drone, height=220)

    st.markdown("<hr style='margin-top: 3px; margin-bottom: 3px;'>", unsafe_allow_html=True)

    # People Found Table and Compact Buttons
    col_table, col_buttons = st.columns([2, 1])
    
    with col_table:
        people_data = [
            {"Name": "Person1", "Location": "34.0522° N, 118.2437° W"},
            {"Name": "Person2", "Location": "36.7783° N, 119.4179° W"},
            {"Name": "Person3", "Location": "40.7128° N, 74.0060° W"},
            {"Name": "Person4", "Location": "34.0522° N, 118.2437° W"},
            {"Name": "Person5", "Location": "51.5074° N, 0.1278° W"},
        ]
        df_people = pd.DataFrame(people_data)
        st.dataframe(df_people, height=220)

    with col_buttons:
        # Round Buttons with Different Colors (CSS Styling)
        button_styles = """
        <style>
        .round-button {
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;  /* Changed to rectangular shape */
            width: 100%;  /* Full width */
            height: 50px;
            margin: -8px auto;
            font-size: 14px;
            border: none;
            cursor: pointer;
            margin-bottom: 5px;  /* Adding space between buttons */
        }
        .start-button {
            background-color: #28a745; /* Green */
            color: white;
        }
        .start-button:hover {
            background-color: #218838;
        }
        .stop-button {
            background-color: #dc3545; /* Red */
            color: white;
        }
        .stop-button:hover {
            background-color: #c82333;
        }
        .fall-button {
            background-color: #ffc107; /* Yellow */
            color: black;
        }
        .fall-button:hover {
            background-color: #e0a800;
        }
        .return-button {
            background-color: #007BFF; /* Blue */
            color: white;
        }
        .return-button:hover {
            background-color: #0056b3;
        }
        .h-button {
            background-color: #17a2b8; /* Cyan */
            color: white;
        }
        .h-button:hover {
            background-color: #138496;
        }
        </style>
        """
        st.markdown(button_styles, unsafe_allow_html=True)

        # Adding Buttons Vertically with Less Margin
        st.markdown("<button class='round-button'>Start</button>", unsafe_allow_html=True)  # Start
        st.markdown("<button class='round-button'>Stop</button>", unsafe_allow_html=True)  # Stop
        st.markdown("<button class='round-button'>Wake</button>", unsafe_allow_html=True)  # Wake Up
        st.markdown("<button class='round-button'>E.S</button>", unsafe_allow_html=True)  # Emergency Stop

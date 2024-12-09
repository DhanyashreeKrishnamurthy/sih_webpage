import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Global Styles
st.set_page_config(layout="wide", page_title="Drone Search and Rescue Dashboard")

# Sidebar for simulation upload
st.sidebar.title("Simulation Panel")
uploaded_file = st.sidebar.file_uploader("Upload Simulation File", type=["mp4", "avi"])
if uploaded_file is not None:
    st.sidebar.video(uploaded_file)
else:
    st.sidebar.write("Upload a simulation file to view here.")

# Sidebar: About Section
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Main Page Layout
st.title("Drone Search and Rescue Dashboard")

# Drone Status Table
st.markdown("### Drone Status")
drone_data = [
    {"Drone ID": "Drone-1", "Battery (%)": 85, "Status": "Active"},
    {"Drone ID": "Drone-2", "Battery (%)": 90, "Status": "Active"},
    {"Drone ID": "Drone-3", "Battery (%)": 45, "Status": "Down"},
    {"Drone ID": "Drone-4", "Battery (%)": 60, "Status": "Active"},
    {"Drone ID": "Drone-5", "Battery (%)": 30, "Status": "Inactive"},
]
df_drone = pd.DataFrame(drone_data)
st.dataframe(df_drone)

# People Found Table
st.markdown("### People Found")
people_data = [
    {"Name": "John Doe", "Location": "Sector A"},
    {"Name": "Jane Smith", "Location": "Sector C"},
    {"Name": "Emily Davis", "Location": "Sector B"},
    {"Name": "Michael Brown", "Location": "Sector A"},
    {"Name": "Anna White", "Location": "Sector D"},
]
df_people = pd.DataFrame(people_data)
st.dataframe(df_people)

# Interactive Map with Basemap Selection
st.markdown("### Interactive Map")
col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)
    m.to_streamlit(height=700)

# Buttons Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Start"):
        st.write("Start button clicked!")

with col2:
    if st.button("Stop"):
        st.write("Stop button clicked!")

with col3:
    if st.button("Wake Up"):
        st.write("Wake Up button clicked!")

with col4:
    if st.button("Emergency Stop"):
        st.write("Emergency Stop button clicked!")
import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

# Global Styles
st.set_page_config(layout="wide", page_title="Drone Search and Rescue Dashboard")

# Sidebar for simulation upload
st.sidebar.title("Simulation Panel")
uploaded_file = st.sidebar.file_uploader("Upload Simulation File", type=["mp4", "avi"])
if uploaded_file is not None:
    st.sidebar.video(uploaded_file)
else:
    st.sidebar.write("Upload a simulation file to view here.")

# Sidebar: About Section
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Main Page Layout
st.title("Drone Search and Rescue Dashboard")

# Drone Status Table
st.markdown("### Drone Status")
drone_data = [
    {"Drone ID": "Drone-1", "Battery (%)": 85, "Status": "Active"},
    {"Drone ID": "Drone-2", "Battery (%)": 90, "Status": "Active"},
    {"Drone ID": "Drone-3", "Battery (%)": 45, "Status": "Down"},
    {"Drone ID": "Drone-4", "Battery (%)": 60, "Status": "Active"},
    {"Drone ID": "Drone-5", "Battery (%)": 30, "Status": "Inactive"},
]
df_drone = pd.DataFrame(drone_data)
st.dataframe(df_drone)

# People Found Table
st.markdown("### People Found")
people_data = [
    {"Name": "John Doe", "Location": "Sector A"},
    {"Name": "Jane Smith", "Location": "Sector C"},
    {"Name": "Emily Davis", "Location": "Sector B"},
    {"Name": "Michael Brown", "Location": "Sector A"},
    {"Name": "Anna White", "Location": "Sector D"},
]
df_people = pd.DataFrame(people_data)
st.dataframe(df_people)

# Interactive Map with Basemap Selection
st.markdown("### Interactive Map")
col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)
    m.to_streamlit(height=700)

# Buttons Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Start"):
        st.write("Start button clicked!")

with col2:
    if st.button("Stop"):
        st.write("Stop button clicked!")

with col3:
    if st.button("Wake Up"):
        st.write("Wake Up button clicked!")

with col4:
    if st.button("Emergency Stop"):
        st.write("Emergency Stop button clicked!")

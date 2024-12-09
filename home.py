import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import base64
from io import BytesIO

# Global Styles
st.set_page_config(layout="wide", page_title="Drone Search and Rescue Dashboard")

# Simulation Panel
st.sidebar.title("Simulation Panel")
uploaded_file = st.sidebar.file_uploader("Upload Simulation File", type=["mp4", "avi"])
if uploaded_file is not None:
    st.sidebar.video(uploaded_file)
else:
    st.sidebar.write("Upload a simulation file to view here.")

# Right Side: Drone Status Table
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

# Right Side: People Found Table
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

# Interactive Map
st.markdown("### Interactive Map")
map_ = leafmap.Map(center=[28.6139, 77.2090], zoom=13)
map_.add_marker([28.6139, 77.2090], popup="Welcome to New Delhi! Capital of India")
map_.to_streamlit(height=500)

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

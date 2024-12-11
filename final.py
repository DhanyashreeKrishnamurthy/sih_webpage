import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import airsim
import numpy as np
import cv2

# Function to get AirSim drone camera feed
def get_airsim_camera_feed(client, camera_name='0', vehicle_name=''):
    """
    Retrieve camera feed from AirSim drone
    
    :param client: AirSim client connection
    :param camera_name: Camera name/index (default '0')
    :param vehicle_name: Name of the drone (if using multiple drones)
    :return: OpenCV image frame
    """
    try:
        # Get image from AirSim
        responses = client.simGetImages([airsim.ImageRequest(camera_name, airsim.ImageType.Scene, False, False)], vehicle_name)
        
        # Check if we got a response
        if responses and len(responses) > 0:
            response = responses[0]
            
            # Convert to numpy array
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            
            # Reshape image
            img_rgb = img1d.reshape(response.height, response.width, 3)
            
            return img_rgb
    except Exception as e:
        st.error(f"Error retrieving AirSim camera feed: {e}")
    
    return None

# Global Styles
st.set_page_config(layout="wide", page_title="Drone Search and Rescue Dashboard")

# Connect to AirSim
try:
    client = airsim.MultirotorClient()
    client.confirmConnection()
except Exception as e:
    st.error(f"Could not connect to AirSim: {e}")
    client = None

# Page Layout
left, right = st.columns([3, 1])  # 75% (left) and 25% (right)

# Left Column (75%)
with left:
    # ELEEVATE Header
    st.markdown("<h1 style='text-align: center;'>ELEEVATE</h1>", unsafe_allow_html=True)

    # Row 1: Simulation Panel - Two Boxes
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        st.write("AirSim Drone 1 Camera Feed")
        
        # Placeholder for camera feed
        airsim_feed_placeholder = st.empty()
        
        # Button to start/stop camera feed
        if st.button('Toggle AirSim Camera Feed'):
            if client:
                # Continuously update the camera feed
                while True:
                    # Get frame from AirSim
                    frame = get_airsim_camera_feed(client, camera_name='0', vehicle_name='Drone1')
                    
                    if frame is not None:
                        # Convert BGR to RGB (OpenCV uses BGR by default)
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Display the frame
                        airsim_feed_placeholder.image(frame_rgb, channels="RGB")
                    
                    # Optional: Add a small delay
                    st.empty()
            else:
                st.error("AirSim client not connected")
    
    with col_sim2:
        uploaded_file2 = st.file_uploader("Upload Simulation 2", type=["mp4", "avi"])  # No title for file uploader
        if uploaded_file2 is not None:
            st.video(uploaded_file2, format="mp4", start_time=0)
    
    # Rest of the code remains the same as in the original script...
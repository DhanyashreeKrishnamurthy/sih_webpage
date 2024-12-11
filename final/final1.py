import gradio as gr
import airsim
import numpy as np
from PIL import Image
import folium
from folium.plugins import MarkerCluster
import leafmap.foliumap as leafmap

# AirSim handler class to interact with the drone
class AirSimHandler:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()

    def get_latest_frame(self):
        # Get the latest frame from the camera
        image = self.client.simGetCameraImage(0, airsim.ImageType.Scene)
        if image:
            raw_img = np.frombuffer(image.image_data_uint8, dtype=np.uint8)
            return Image.fromarray(raw_img.reshape(image.height, image.width, 3))
        return None

# Initialize the AirSim handler
airsim_handler = AirSimHandler()

# Function to fetch the latest frame
def update_camera_feed():
    try:
        # Get the latest frame
        latest_frame = airsim_handler.get_latest_frame()
        
        if latest_frame is not None:
            return latest_frame
        return None
    except Exception as e:
        print(f"Error updating camera feed: {e}")
        return None

# Function to create a simple Folium map centered around a specific location (Bangalore for example)
def create_map():
    # Create a map centered around Bangalore
    map_center = [12.9716, 77.5946]  # Coordinates for Bangalore
    folium_map = folium.Map(location=map_center, zoom_start=12)

    # Add a marker cluster to the map
    marker_cluster = MarkerCluster().add_to(folium_map)

    # Example marker (You can add real drone coordinates here)
    folium.Marker([12.9716, 77.5946], popup="Bangalore").add_to(marker_cluster)

    return folium_map

# Create the dashboard interface
def create_dashboard():
    return """
    <div style="text-align: center;">
        <h2>Drone Camera Feed</h2>
        <p>Click the button to start the drone camera feed.</p>
    </div>
    """

# Main function for Gradio interface setup
def main():
    with gr.Blocks() as demo:
        # Create dashboard HTML
        dashboard_html = gr.HTML(create_dashboard())
        
        # Image output for camera feed
        camera_feed = gr.Image(label="Drone Camera Feed")
        
        # Folium map output
        folium_map_output = gr.HTML()

        # Button to start the drone feed
        start_btn = gr.Button("Start Drone Feed")
        
        # Connect button click to the camera feed update function
        start_btn.click(fn=update_camera_feed, outputs=camera_feed)
        
        # Periodic update for the camera feed every second
        demo.load(fn=update_camera_feed, outputs=camera_feed, every=1)

        # Display Folium map in the Gradio interface
        demo.load(fn=create_map, outputs=folium_map_output)

    # Launch the Gradio interface
    demo.launch(server_name='127.0.0.1', server_port=7860)

if __name__ == "__main__":
    main()

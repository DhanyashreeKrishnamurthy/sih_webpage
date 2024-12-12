import gradio as gr
import airsim
import numpy as np
from PIL import Image
import folium
from folium.plugins import MarkerCluster
import leafmap.foliumap as leafmap
import threading
import time

class AirSimHandler:
    def __init__(self):
        try:
            self.client = airsim.MultirotorClient()
            self.client.confirmConnection()
            self.client.enableApiControl(True)
            self.current_position = None
            self.is_flying = False
            print("AirSim connection established successfully.")
        except Exception as e:
            print(f"Error connecting to AirSim: {e}")
            self.client = None

    def get_latest_frame(self):
        """Retrieve the latest camera frame from the drone"""
        try:
            image = self.client.simGetCameraImage(0, airsim.ImageType.Scene)
            if image:
                raw_img = np.frombuffer(image.image_data_uint8, dtype=np.uint8)
                return Image.fromarray(raw_img.reshape(image.height, image.width, 3))
            return None
        except Exception as e:
            print(f"Error getting camera frame: {e}")
            return None

    def get_drone_position(self):
        """Get current GPS coordinates of the drone"""
        try:
            gps_data = self.client.getGpsData(gps_name='')
            return [gps_data.gnss.latitude, gps_data.gnss.longitude]
        except Exception as e:
            print(f"Error getting drone position: {e}")
            return None

    def takeoff(self, altitude=10):
        """Initiate drone takeoff"""
        try:
            self.client.armDisarm(True)
            self.client.takeoffAsync().join()
            self.is_flying = True
            print(f"Drone taking off to {altitude} meters")
        except Exception as e:
            print(f"Takeoff error: {e}")

    def land(self):
        """Land the drone"""
        try:
            self.client.landAsync().join()
            self.client.armDisarm(False)
            self.is_flying = False
            print("Drone landing")
        except Exception as e:
            print(f"Landing error: {e}")

    def move_drone(self, direction, distance=10):
        """Move drone in specified direction"""
        try:
            if direction == 'forward':
                self.client.moveByVelocityAsync(distance, 0, 0, 1).join()
            elif direction == 'backward':
                self.client.moveByVelocityAsync(-distance, 0, 0, 1).join()
            elif direction == 'left':
                self.client.moveByVelocityAsync(0, -distance, 0, 1).join()
            elif direction == 'right':
                self.client.moveByVelocityAsync(0, distance, 0, 1).join()
            print(f"Moving drone {direction}")
        except Exception as e:
            print(f"Movement error: {e}")

class DroneDashboard:
    def __init__(self):
        self.airsim_handler = AirSimHandler()
        self.drone_map = None
        self.marker_cluster = None
        self.track_positions = []

    def create_map(self):
        """Create an interactive Folium map"""
        # Default to Bangalore if no drone position
        default_location = [12.9716, 77.5946]
        
        # Try to get current drone position
        current_pos = self.airsim_handler.get_drone_position()
        map_center = current_pos if current_pos else default_location

        self.drone_map = folium.Map(location=map_center, zoom_start=12)
        self.marker_cluster = MarkerCluster().add_to(self.drone_map)

        # Add drone position marker
        if current_pos:
            folium.Marker(
                current_pos, 
                popup="Current Drone Position", 
                icon=folium.Icon(color='red', icon='plane')
            ).add_to(self.marker_cluster)

        # Track drone path
        if self.track_positions:
            folium.PolyLine(
                locations=self.track_positions, 
                color='blue', 
                weight=2, 
                opacity=0.8
            ).add_to(self.drone_map)

        # Convert map to HTML
        return self.drone_map._repr_html_()

    def update_drone_position(self):
        """Update drone position on map"""
        pos = self.airsim_handler.get_drone_position()
        if pos:
            self.track_positions.append(pos)
        return self.create_map()

    def create_dashboard(self):
        """Create dashboard interface"""
        return """
        <div style="text-align: center; background-color: #f0f0f0; padding: 20px;">
            <h2>Drone Control Dashboard</h2>
            <p>Advanced drone monitoring and control system</p>
            <div style="color: green;">Status: Connected to AirSim</div>
        </div>
        """

def main():
    drone_dashboard = DroneDashboard()

    with gr.Blocks() as demo:
        # Dashboard HTML
        dashboard_html = gr.HTML(drone_dashboard.create_dashboard())
        
        # Camera Feed
        camera_feed = gr.Image(label="Drone Camera Feed")
        
        # Map Output
        folium_map_output = gr.HTML(drone_dashboard.create_map())

        # Control Buttons
        with gr.Row():
            takeoff_btn = gr.Button("Takeoff")
            land_btn = gr.Button("Land")

        with gr.Row():
            forward_btn = gr.Button("Forward")
            backward_btn = gr.Button("Backward")
            left_btn = gr.Button("Left")
            right_btn = gr.Button("Right")

        # Button Click Handlers
        takeoff_btn.click(
            fn=drone_dashboard.airsim_handler.takeoff, 
            outputs=None
        )
        land_btn.click(
            fn=drone_dashboard.airsim_handler.land, 
            outputs=None
        )

        # Movement Button Handlers
        forward_btn.click(
            fn=lambda: drone_dashboard.airsim_handler.move_drone('forward'), 
            outputs=None
        )
        backward_btn.click(
            fn=lambda: drone_dashboard.airsim_handler.move_drone('backward'), 
            outputs=None
        )
        left_btn.click(
            fn=lambda: drone_dashboard.airsim_handler.move_drone('left'), 
            outputs=None
        )
        right_btn.click(
            fn=lambda: drone_dashboard.airsim_handler.move_drone('right'), 
            outputs=None
        )

        # Periodic Updates
        demo.load(
            fn=drone_dashboard.airsim_handler.get_latest_frame, 
            outputs=camera_feed, 
            every=1
        )
        demo.load(
            fn=drone_dashboard.update_drone_position, 
            outputs=folium_map_output, 
            every=2
        )

    # Launch the Gradio interface
    demo.launch(server_name='127.0.0.1', server_port=7860)

if __name__ == "__main__":
    main()
import airsim
import numpy as np
import cv2
import gradio as gr
import threading
import queue
import time
import folium
import leafmap.foliumap as leafmap
from io import BytesIO
import base64

# AirSim Camera Handler Class (Previous implementation remains the same)
class AirSimCameraHandler:
    def __init__(self):
        self.frame_queue = queue.Queue(maxsize=1)
        self.stop_event = threading.Event()
        self.thread = None
        self.client = None

    def connect_airsim(self):
        """Establish connection to AirSim"""
        try:
            self.client = airsim.MultirotorClient()
            self.client.confirmConnection()
            print("AirSim Connected Successfully")
            return True
        except Exception as e:
            print(f"AirSim Connection Error: {e}")
            return False

    def capture_frames(self):
        """Thread function to capture frames"""
        try:
            while not self.stop_event.is_set():
                # Capture frame from AirSim
                responses = self.client.simGetImages([airsim.ImageRequest(
                    '0', airsim.ImageType.Scene, False, False
                )])

                if responses and len(responses) > 0:
                    response = responses[0]
                    
                    # Convert to numpy array
                    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
                    
                    # Reshape and convert color
                    img_rgb = cv2.cvtColor(
                        img1d.reshape(response.height, response.width, 3), 
                        cv2.COLOR_BGR2RGB
                    )
                    
                    # Clear queue if full
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                    
                    self.frame_queue.put(img_rgb)
                
                time.sleep(0.1)  # Prevent overwhelming
        except Exception as e:
            print(f"Frame Capture Error: {e}")

    def start_capture(self):
        """Start the camera capture thread"""
        # Ensure AirSim connection is established
        if not self.client:
            if not self.connect_airsim():
                return False
        
        # If thread is already running, don't start again
        if self.thread and self.thread.is_alive():
            return True
        
        # Clear any existing stop event
        self.stop_event.clear()
        
        # Create and start the thread
        self.thread = threading.Thread(target=self.capture_frames)
        self.thread.daemon = True
        self.thread.start()
        return True

    def stop_capture(self):
        """Stop the camera capture thread"""
        if self.thread:
            self.stop_event.set()
            self.thread.join()
            self.thread = None

    def get_latest_frame(self):
        """Get the latest frame from the queue"""
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None

# Global AirSim handler
airsim_handler = AirSimCameraHandler()

def create_interactive_map():
    """Create an interactive Folium map"""
    # Default location (can be modified based on actual drone deployment)
    map_ = leafmap.Map(center=[28.6139, 77.2090], zoom=13)
    map_.add_marker([28.6139, 77.2090], popup="Welcome to New Delhi! Capital of India")
    map_.to_streamlit(height=500)
    # m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)
    
    # Add markers for drone locations
    drone_locations = [
        {"id": "Drone-1", "lat": 37.7749, "lon": -122.4194, "status": "Active", "battery": 75},
        {"id": "Drone-2", "lat": 37.7800, "lon": -122.4250, "status": "Active", "battery": 90},
        {"id": "Drone-3", "lat": 37.7700, "lon": -122.4150, "status": "Inactive", "battery": 60}
    ]
    
    # Color coding based on drone status
    for drone in drone_locations:
        color = 'green' if drone['status'] == 'Active' else 'red'
        popup_text = f"""
        Drone: {drone['id']}
        Status: {drone['status']}
        Battery: {drone['battery']}%
        """
        folium.Marker(
            location=[drone['lat'], drone['lon']],
            popup=popup_text,
            icon=folium.Icon(color=color, icon='plane')
        ).add_to(map_)
    
    # People found markers
    people_locations = [
        {"name": "John", "lat": 37.7749, "lon": -122.4200, "location": "Sector 1"},
        {"name": "Anna", "lat": 37.7800, "lon": -122.4230, "location": "Sector 2"}
    ]
    
    for person in people_locations:
        popup_text = f"""
        Name: {person['name']}
        Location: {person['location']}
        """
        folium.Marker(
            location=[person['lat'], person['lon']],
            popup=popup_text,
            icon=folium.Icon(color='blue', icon='user')
        ).add_to(map_)
    
    # Save map to HTML
    map_html = map_.get_root().render()
    
    return map_html

def create_dashboard():
    """Create the main dashboard layout"""
    # Drone Status Table
    drone_data = [
        {"Drone ID": "Drone-1", "Battery (%)": 75, "Status": "Active"},
        {"Drone ID": "Drone-2", "Battery (%)": 90, "Status": "Active"},
        {"Drone ID": "Drone-3", "Battery (%)": 60, "Status": "Inactive"},
        {"Drone ID": "Drone-4", "Battery (%)": 50, "Status": "Active"},
        {"Drone ID": "Drone-5", "Battery (%)": 40, "Status": "Inactive"},
    ]

    # People Found Table
    people_data = [
        {"Name": "John", "Location": "Sector 1"},
        {"Name": "Anna", "Location": "Sector 2"},
        {"Name": "Tom", "Location": "Sector 3"},
        {"Name": "Kate", "Location": "Sector 4"},
        {"Name": "Emma", "Location": "Sector 5"},
    ]

    # Generate HTML for dashboard
    dashboard_html = f"""
    <div style="display: flex; flex-direction: column; width: 100%;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
            <div style="width: 60%; margin-right: 20px;">
                <h2>Drone Camera Feed</h2>
                <div style="border: 1px solid #ddd; padding: 10px;">
                    <img id="camera-feed" src="" style="max-width: 100%; max-height: 400px; background-color: #f0f0f0;">
                </div>
                
                <h2>Interactive Map</h2>
                <div style="border: 1px solid #ddd; padding: 10px; height: 400px; overflow: auto;">
                    {create_interactive_map()}
                </div>
            </div>
            
            <div style="width: 35%;">
                <div style="margin-bottom: 20px;">
                    <h3>Drone Status</h3>
                    <table border="1" style="width: 100%;">
                        <tr>
                            <th>Drone ID</th>
                            <th>Battery (%)</th>
                            <th>Status</th>
                        </tr>
                        {''.join(f'<tr><td>{d["Drone ID"]}</td><td>{d["Battery (%)"]}</td><td>{d["Status"]}</td></tr>' for d in drone_data)}
                    </table>
                </div>
                
                <div>
                    <h3>People Found</h3>
                    <table border="1" style="width: 100%;">
                        <tr>
                            <th>Name</th>
                            <th>Location</th>
                        </tr>
                        {''.join(f'<tr><td>{p["Name"]}</td><td>{p["Location"]}</td></tr>' for p in people_data)}
                    </table>
                </div>
            </div>
        </div>
    </div>
    """
    
    return dashboard_html

def update_camera_feed():
    """Update camera feed in the dashboard"""
    try:
        # Ensure AirSim capture is started
        airsim_handler.start_capture()
        
        # Get latest frame
        latest_frame = airsim_handler.get_latest_frame()
        
        if latest_frame is not None:
            return latest_frame
        return None
    except Exception as e:
        print(f"Error updating camera feed: {e}")
        return None

def main():
    # Create Gradio interface
    with gr.Blocks() as demo:
        # Full Dashboard HTML
        dashboard_html = gr.HTML(create_dashboard())
        
        # Camera feed update
        camera_feed = gr.Image(label="Drone Camera Feed")
        
        # Interactive Map
        interactive_map = gr.HTML(label="Drone Deployment Map")
        
        # Start button to begin drone feed
        start_btn = gr.Button("Start Drone Feed")
        start_btn.click(
            fn=update_camera_feed, 
            outputs=camera_feed
        )
        
        # Update map button
        update_map_btn = gr.Button("Update Map")
        update_map_btn.click(
            fn=create_interactive_map,
            outputs=interactive_map
        )
        
        # Periodic update
        demo.load(update_camera_feed, outputs=camera_feed, every=1)

    # Launch the demo
    demo.launch(server_name='127.0.0.1', server_port=7860)

if __name__ == "__main__":
    main()
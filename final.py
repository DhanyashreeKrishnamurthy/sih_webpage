import gradio as gr
import airsim
import numpy as np
import cv2
import threading
import queue
import time

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
                responses = self.client.simGetImages([
                    airsim.ImageRequest('0', airsim.ImageType.Scene, False, False)
                ])
                
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
        if not self.client:
            if not self.connect_airsim():
                return False
        
        self.stop_event.clear()
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

    return f"""
    <div style="display: flex; justify-content: space-between;">
        <div style="width: 60%;">
            <h2>Drone Camera Feed</h2>
            <img id="camera-feed" src="" style="max-width: 100%; max-height: 400px;">
        </div>
        <div style="width: 35%;">
            <h3>Drone Status</h3>
            <table border="1">
                <tr>
                    <th>Drone ID</th>
                    <th>Battery (%)</th>
                    <th>Status</th>
                </tr>
                {''.join(f'<tr><td>{d["Drone ID"]}</td><td>{d["Battery (%)"]}</td><td>{d["Status"]}</td></tr>' for d in drone_data)}
            </table>
            
            <h3>People Found</h3>
            <table border="1">
                <tr>
                    <th>Name</th>
                    <th>Location</th>
                </tr>
                {''.join(f'<tr><td>{p["Name"]}</td><td>{p["Location"]}</td></tr>' for p in people_data)}
            </table>
        </div>
    </div>
    """

def update_camera_feed():
    """Update camera feed in the dashboard"""
    try:
        # Start capture if not already running
        if not hasattr(airsim_handler, 'thread') or not airsim_handler.thread:
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
        # Dashboard HTML
        dashboard_html = gr.HTML(create_dashboard())
        
        # Camera feed update
        camera_feed = gr.Image(label="Drone Camera Feed")
        
        # Start button to begin drone feed
        start_btn = gr.Button("Start Drone Feed")
        start_btn.click(
            fn=update_camera_feed, 
            outputs=camera_feed
        )
        
        # Periodic update
        demo.load(update_camera_feed, outputs=camera_feed, every=1)

    # Launch the demo
    demo.launch(server_name='127.0.0.1', server_port=7860)

if __name__ == "__main__":
    main()
import airsim
import numpy as np
import cv2
import threading
import queue
import time
import gradio as gr
from IPython.display import IFrame
from ultralytics import RTDETR

# Load the YOLO model
model = RTDETR("rtdetr.pt")

# AirSim Camera Handler Class
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
    """Generate an OpenStreetMap HTML iframe"""
    iframe = IFrame(
        src="https://www.openstreetmap.org/export/embed.html?bbox=77.2000%2C28.6100%2C77.2200%2C28.6200&layer=mapnik",
        width="100%",
        height="400"
    )
    return iframe._repr_html_()

def update_camera_feed():
    """Update camera feed and run detection on it"""
    try:
        # Ensure AirSim capture is started
        airsim_handler.start_capture()
        
        # Get latest frame
        latest_frame = airsim_handler.get_latest_frame()
        
        if latest_frame is not None:
            # Run object detection on the frame
            results = model.predict(latest_frame, show=True, classes=[0])  # Assuming class 0 for detection
            
            # Process the result, add annotations (bounding boxes, etc.) to the frame
            annotated_frame = results[0].plot()  # Assuming results is a list of detections
            return annotated_frame
        
        return None
    except Exception as e:
        print(f"Error updating camera feed: {e}")
        return None

def main():
    # Create Gradio interface
    with gr.Blocks() as demo:
        with gr.Row():  # Use a Row for side-by-side layout
            camera_feed = gr.Image(label="Drone Camera Feed", elem_id="camera_feed")
            interactive_map_html = gr.HTML(label="Interactive Map", elem_id="interactive_map")
        
        drone_status = gr.Dataframe(
            headers=["Drone ID", "Battery (%)", "Status"],
            value=[["Drone-1", 75, "Active"], ["Drone-2", 90, "Active"], ["Drone-3", 60, "Inactive"]],
            label="Drone Status"
        )

        people_found = gr.Dataframe(
            headers=["Name", "Location"],
            value=[["John", "Sector 1"], ["Anna", "Sector 2"]],
            label="People Found"
        )

        start_btn = gr.Button("Start Drone Feed")
        start_btn.click(
            fn=update_camera_feed, 
            outputs=camera_feed
        )

        update_map_btn = gr.Button("Update Map")
        update_map_btn.click(
            fn=create_interactive_map,
            outputs=interactive_map_html
        )

        demo.load(update_camera_feed, outputs=camera_feed, every=1)

    # Launch the demo
    demo.launch(server_name='127.0.0.1', server_port=7860)

if __name__ == "__main__":
    main()

import airsim
import numpy as np
import cv2
import threading
import queue
import time
import gradio as gr

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
    """Generate an OpenLayers-based interactive map"""
    map_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenLayers Map</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@latest/ol.css">
        <script src="https://cdn.jsdelivr.net/npm/ol@latest/ol.js"></script>
        <style>
            #map {
                width: 100%;
                height: 400px;
            }
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = new ol.Map({
                target: 'map',
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM()
                    })
                ],
                view: new ol.View({
                    center: ol.proj.fromLonLat([77.216721, 28.6448]), // Default coordinates
                    zoom: 14
                })
            });

            // Add interaction for area selection
            var select = new ol.interaction.Select();
            map.addInteraction(select);

            var dragBox = new ol.interaction.DragBox();
            map.addInteraction(dragBox);

            dragBox.on('boxend', function() {
                var extent = dragBox.getGeometry().getExtent();
                alert('Selected area: ' + extent.join(', '));
            });

            dragBox.on('boxstart', function() {
                console.log('Box selection started');
            });
        </script>
    </body>
    </html>
    """
    return map_html

def main():
    # Create Gradio interface
    with gr.Blocks() as demo:
        live_feed = gr.Image(label="Live Drone Feed")

        drone_status = gr.Dataframe(
            headers=["Drone ID", "Battery (%)", "Status"],
            value=[
                ["Drone-1", 75, "Active"],
                ["Drone-2", 90, "Active"],
                ["Drone-3", 60, "Inactive"]
            ],
            label="Drone Status"
        )

        people_found = gr.Dataframe(
            headers=["Name", "Location"],
            value=[
                ["John", "Sector 1"],
                ["Anna", "Sector 2"]
            ],
            label="People Found"
        )

        update_feed_btn = gr.Button("Get Live Feed")
        update_feed_btn.click(
            fn=lambda: airsim_handler.get_latest_frame(),
            outputs=live_feed
        )

    # Launch the demo
    demo.launch(server_name='127.0.0.1', server_port=7860)

if __name__ == "__main__":
    main()

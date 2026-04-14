#this is the code implemented by the main program responsible for object detection 
#via the jetson inference/utils library
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import cv2
import numpy as np
import time
import datetime

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=2,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (#Gives the conditions of the camera, can be selectively edited if so desired
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

net = detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = videoSource("csi://0")
display = videoOutput("display://0")

while display.IsStreaming():
    img = camera.Capture()

    if img is None:
        continue

    detections = net.Detect(img)
    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    
    
    
    

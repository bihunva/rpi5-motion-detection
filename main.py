import time
import os
from gpiozero import MotionSensor, LED
from picamzero import Camera
from signal import pause
from pathlib import Path

# PINs
PIR_PIN = 4
LED_PIN = 17

# Global variables
MOTION_DURATION_THRESHOLD = 5.0
MIN_DURATION_BETWEEN_PHOTOS = 30.0
CAMERA_FOLDER_PATH = Path("/home/pi/Desktop/projects/rpi5-motion-detection/photos")
time_motion_started = time.time()
last_time_photo_taken = 0

# Setup GPIOs
pir = MotionSensor(PIR_PIN)
led = LED(LED_PIN)
print("GPIOs setup OK")

# Setup camera
camera = Camera()
time.sleep(2)
os.makedirs(CAMERA_FOLDER_PATH, exist_ok=True)
print("Camera setup OK")

def create_photo(camera, folder_path):
    print("Taking a photo")
    file_name = CAMERA_FOLDER_PATH / f"img_{time.time()}.jpg"
    camera.take_photo(file_name)
    print(f"Photo saved at: {file_name}")

def motion_detected():
    print("Starting timer")
    global time_motion_started
    time_motion_started = time.time()
    led.on()
    
def motion_finished():
    led.off()
    global last_time_photo_taken
    
    motion_duration = time.time() - time_motion_started
    print(f"Motion duration: {motion_duration}")
    
    if motion_duration > MOTION_DURATION_THRESHOLD:
        if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_PHOTOS:
            last_time_photo_taken = time.time()
            create_photo(camera=camera, folder_path=CAMERA_FOLDER_PATH)
            
    

pir.when_motion = motion_detected
pir.when_no_motion = motion_finished

pause()

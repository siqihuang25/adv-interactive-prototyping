import os, sys, io
import M5
from M5 import *
from unit import IMUProUnit
import time
from hardware import *
import m5utils

print('IMU and LED - 3 Modes')

M5.begin()

# Configure I2C on PortA (red connector)
i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=50000)

# Initialize IMU Pro unit
imupro_0 = IMUProUnit(i2c0)

# Configure RGB strip on pin 7 with 30 LEDs
rgb_strip = RGB(io=7, n=30, type="SK6812")

# Function to set all LEDs to a color
def set_led_color(r, g, b):
    rgb_color = (r << 16) | (g << 8) | b
    rgb_strip.fill_color(rgb_color)

# Function to create a pulsing wave effect for "Hello" gesture
def wave_effect():
    for brightness in range(0, 256, 10):  
        set_led_color(brightness, 0, brightness)  
        time.sleep(0.05)
    for brightness in range(255, -1, -10): 
        set_led_color(brightness, 0, brightness)
        time.sleep(0.05)

# Function for synchronized motion effect
def sync_effect():
    for i in range(3):  
        set_led_color(0, 255, 0)  
        time.sleep(0.2)
        set_led_color(0, 0, 0)  
        time.sleep(0.2)

# Define thresholds and variables for modes
shake_threshold = 1.5  
sync_threshold = 0.5  
last_motion_time = time.time()
in_sync_mode = False  

while True:
    M5.update()
    
    # Get accelerometer data
    imu_data = imupro_0.get_accelerometer()
    acc_x = imu_data[0]
    acc_y = imu_data[1]
    acc_z = imu_data[2]
    
    # Print accelerometer data for debugging
    print(acc_x, ',', acc_y, ',', acc_z)
    
    # Mode 1: Quick Shake (Hello) Detection based on Y-axis
    if abs(acc_y) > shake_threshold:
        print("Shake detected on Y-axis - Hello!")
        wave_effect()  
        last_motion_time = time.time()
        in_sync_mode = False  
    
    # Mode 2: Synchronized Motion based on X-axis
    elif abs(acc_x) > sync_threshold:
        if not in_sync_mode:
            print("Synchronized movement detected on X-axis - Sync mode")
            sync_effect()  
            in_sync_mode = True  
        last_motion_time = time.time()  
    
    # Mode 3: Ambient Stillness Mode
    elif time.time() - last_motion_time > 5:  # No motion for 5 seconds
        print("No motion - Ambient mode")
        set_led_color(255, 80, 0) 
        in_sync_mode = False  
    
    time.sleep(0.05)  

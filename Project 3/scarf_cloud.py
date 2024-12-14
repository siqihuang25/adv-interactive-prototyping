import os, sys, io
import M5
from M5 import *
from hardware import *
import time
import network
from umqtt import *
from unit import ToFUnit

M5.begin()

# Configure RGB strip connected to pin 2 with 30 LEDs enabled:
rgb = RGB(io=7, n=30, type="SK6812")
rgb.fill_color(0)  # Turn off LEDs initially
rgb.set_brightness(50)  # Set initial brightness to 50%

# ToF distance sensor setup
i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
tof_0 = ToFUnit(i2c0)

ssid = 'wifi_name'
password = 'wifi_password'

mqtt_client = None
aio_user_name = 'aio_username'
aio_password = 'aio_key'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print('Connecting to WiFi...')
while not wifi.isconnected():
    print('.', end='')
    time.sleep_ms(100)

print('WiFi connection successful')
ip_list = wifi.ifconfig()
ip_address = ip_list[0]
print('IP address:', ip_address)

mqtt_client = MQTTClient(
    'testclient_vanessa',
    'io.adafruit.com',
    port=1883,
    user=aio_user_name,
    password=aio_password,
    keepalive=3000
)
mqtt_client.connect(clean_session=True)

# Global variables for Cloud-controlled colors
color = None
scarf_1_color = None

def get_color_from_hexstr(color_str):
    return int(color_str[1:], 16)

def interpolate_colors(colors, ratio):
    """Interpolate between multiple colors."""
    idx = int(ratio * (len(colors) - 1))
    next_idx = min(idx + 1, len(colors) - 1)
    local_ratio = (ratio * (len(colors) - 1)) % 1
    start_color = colors[idx]
    end_color = colors[next_idx]
    r = int(((start_color >> 16) * (1 - local_ratio) + (end_color >> 16) * local_ratio))
    g = int((((start_color >> 8) & 0xFF) * (1 - local_ratio) + ((end_color >> 8) & 0xFF) * local_ratio))
    b = int(((start_color & 0xFF) * (1 - local_ratio) + (end_color & 0xFF) * local_ratio))
    return (r << 16) | (g << 8) | b

# Callback function for receiving color updates
def color_feed_callback(data):
    global color
    color_str = data[1].decode()
    print('Received color:', color_str)
    color = get_color_from_hexstr(color_str)

mqtt_client.subscribe(aio_user_name + '/feeds/color', color_feed_callback)

# Callback function for receiving scarf-1 color updates
def scarf_1_color_callback(data):
    global scarf_1_color
    color_str = data[1].decode()
    print('Received scarf-1 color:', color_str)
    scarf_1_color = get_color_from_hexstr(color_str)

mqtt_client.subscribe(aio_user_name + '/feeds/scarf-1-color', scarf_1_color_callback)

# Callback function for receiving brightness updates
def brightness_feed_callback(data):
    global brightness
    brightness_str = data[1].decode()  # Receive brightness as a string
    print('Received brightness:', brightness_str)
    brightness = int(brightness_str)  # Convert to integer
    rgb.set_brightness(brightness)  # Update the brightness of the RGB strip

mqtt_client.subscribe(aio_user_name + '/feeds/brightness', brightness_feed_callback)

publish_timer = 0
last_distance = None
wave_offset = 0  # Track the wave position

while True:
    M5.update()

    # Check distance
    if time.ticks_ms() > publish_timer + 3000:  # Publish every 3 seconds
        distance = tof_0.get_distance()
        print(f"Distance: {distance} cm")
        mqtt_client.publish(aio_user_name + '/feeds/distance', str(distance), qos=0)
        publish_timer = time.ticks_ms()

        # Ensure colors are set
        if color is None or scarf_1_color is None:
            print("Waiting for Cloud colors...")
            continue

        # Adjust gradient range based on distance
        if distance <= 20:
            colors = [color, scarf_1_color]
        elif distance <= 50:
            mid_color = interpolate_colors([color, scarf_1_color], 0.5)
            colors = [color, mid_color, scarf_1_color]
        else:
            mid_color1 = interpolate_colors([color, scarf_1_color], 0.33)
            mid_color2 = interpolate_colors([color, scarf_1_color], 0.66)
            colors = [color, mid_color1, mid_color2, scarf_1_color]

        # Apply wave effect
        num_leds = 30
        wave_speed = 1  # Pixels per frame
        wave_offset = (wave_offset + wave_speed) % num_leds

        for i in range(num_leds):
            ratio = ((i + wave_offset) % num_leds) / num_leds
            interpolated_color = interpolate_colors(colors, ratio)
            rgb.set_color(i, interpolated_color)  # Use set_color for each LED

        rgb.show()  # Update all LEDs

    mqtt_client.check_msg()
    time.sleep_ms(50)
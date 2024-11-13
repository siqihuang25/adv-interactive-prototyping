import os, sys, io
import M5
from M5 import *
from hardware import *
import time

print('digital input to change RGB colors')

# Initialize M5 board:
M5.begin()

# Configure RGB strip connected to pin 2 with 10 LEDs enabled:
rgb_strip = RGB(io=2, n=10, type="SK6812")

# Initial state is low power mode (light blue color)
initial_color = 0x00ffff  # Light blue
rgb_strip.fill_color(initial_color)  # Set initial color
time.sleep_ms(1000)  # Wait 1 second

# Variable to keep track of program state:
program_state = 'LOW_POWER'  # Initial state

# Configure pin 8 as output:
output_pin = Pin(8, mode=Pin.OUT)

# Configure pin 7 as input that is high by default:
input_pin = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)

# Main loop
while True:  # Infinite loop
    M5.update()  # Update M5 board

    # Check if the lid is opened (copper tape touches)
    if input_pin.value() == False:  # If the input pin is low (copper tape touches)
        if program_state != 'OPEN':  # Only change if not already in OPEN state
            print('Lid opened: changing color to yellow')
            rgb_strip.fill_color(0xffff00)  # Change to yellow
            program_state = 'OPEN'  # Update program state
        
    else:  # Lid is closed (copper tape does not touch)
        if program_state == 'OPEN':  # Only change if previously in OPEN state
            print('Lid closed: returning to initial state (light blue)')
            rgb_strip.fill_color(initial_color)  # Return to light blue (low power mode)
            program_state = 'LOW_POWER'  # Update program state

    time.sleep_ms(100)  # Wait for 100 milliseconds

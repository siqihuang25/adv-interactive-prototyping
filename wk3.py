import os, sys, io
import M5
from M5 import *
from hardware import *
import time
import random

# Initialize M5 board
M5.begin()

# Set up the RGB light strip (Pin 2, 15 LEDs)
rgb_strip = RGB(io=2, n=15, type="SK6812")

# Configure pin 8 as output for additional output needs
output_pin = Pin(8, mode=Pin.OUT)

# Using built-in button (BtnA) as input instead of copper tape
input_pin = BtnA.wasPressed

# Function to set a single color to the entire strip
def fill_strip(color):
    rgb_strip.fill_color(color)

# Function for color-wipe effect (State 1 - Initialization)
def color_wipe(color):
    for i in range(15):
        rgb_strip.set_color(i, color)
        rgb_strip.show()
        time.sleep(0.1)

# Function for breathing effect (State 2 - Waiting)
def breathing_effect(color):
    for brightness in range(0, 255, 5):
        for i in range(15):
            r = (color[0] * brightness) // 255
            g = (color[1] * brightness) // 255
            b = (color[2] * brightness) // 255
            rgb_strip.set_color(i, (r << 16) | (g << 8) | b)
        rgb_strip.show()
        time.sleep(0.02)
    
    # Breathing out
    for brightness in range(255, 0, -5):
        for i in range(15):
            r = (color[0] * brightness) // 255
            g = (color[1] * brightness) // 255
            b = (color[2] * brightness) // 255
            rgb_strip.set_color(i, (r << 16) | (g << 8) | b)
        rgb_strip.show()
        time.sleep(0.02)
    
    # Twinkle effect (random LEDs flash quickly)
    for _ in range(3):  # Repeat 3 times for a twinkle effect
        random_led = random.randint(0, 14)
        rgb_strip.set_color(random_led, 0xFFFFFF)  # Flash white
        rgb_strip.show()
        time.sleep(0.1)
        rgb_strip.set_color(random_led, 0x000000)  # Turn off
        rgb_strip.show()

# Function for chase effect (State 3 - Running)
def chase_effect(color):
    for i in range(15):
        rgb_strip.set_color(i, color)
        rgb_strip.set_color((i - 1) % 15, 0x000000)  # Turn off previous LED
        rgb_strip.show()
        time.sleep(0.1 - i * 0.005)  # Speed up chase over time

# Function for confetti effect (State 4 - Finish)
def confetti_effect():
    for _ in range(20):  # Flash 20 random LEDs
        random_led = random.randint(0, 14)
        random_color = random.randint(0, 0xFFFFFF)  # Random bright colors
        rgb_strip.set_color(random_led, random_color)
        rgb_strip.show()
        time.sleep(0.05)
        rgb_strip.set_color(random_led, 0x000000)  # Turn off
        rgb_strip.show()

# Main function to control the LED patterns
def main():
    program_state = 'INIT'  # Start with the Initialization state
    
    while True:
        M5.update()  # Update M5 system

        # Check if the built-in button (BtnA) was pressed
        if input_pin():  # Button A pressed
            if program_state == 'INIT':
                # State 1: Initialization - Color wipe effect
                print('State: INIT (Color Wipe)')
                color_wipe(0xFFFFFF)  # Wipe with white
                program_state = 'WAITING'  # Move to waiting state
                
            elif program_state == 'WAITING':
                # State 2: Waiting - Breathing effect with twinkle
                print('State: WAITING (Breathing + Twinkle)')
                breathing_effect((0, 255, 255))  # Cyan breathing
                program_state = 'RUNNING'  # Move to running state
                
            elif program_state == 'RUNNING':
                # State 3: Running - Chase effect
                print('State: RUNNING (Chase)')
                chase_effect((255, 0, 0))  # Red chase effect
                program_state = 'FINISH'  # Move to finish state
                
            elif program_state == 'FINISH':
                # Optional State 4: Finish - Confetti effect
                print('State: FINISH (Confetti)')
                confetti_effect()  # Confetti effect
                program_state = 'INIT'  # Restart back to INIT
                
        # Delay to avoid rapid toggling
        time.sleep(0.1)

# Run the main function
main()

### Introduction

My project is an LED scarf that integrates motion detection technology using an IMU Pro sensor and a dynamic LED strip. The scarf responds to various movements with interactive light patterns, creating a fusion of wearable technology and artistic expression.

![Ideation](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/project%202/ideation.jpg)

### State Diagram

Initial state: the default mode when the system is powered on and no significant motion is detected

Waving mode: a quick shake along the Y-axis triggers a pulsing purple wave effect

Synchronizing mode: moderate, sustained motion along the X-axis activates rhythmic green flashes

Resting mode: after 5 seconds of inactivity, the LEDs settle into a steady, warm orangish-yellow glow

![state_diagram](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/project%202/state_diagram.jpg)

### Hardware

* M5Stack Atom Lite  
* Digital RGB LED Weatherproof Strip
* USB-C Cable
* M5Stack IMU Pro

![hardware](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/project%202/hardware.jpg)

### Firmware   

Waiving mode:
``` Python  
def wave_effect():
    for brightness in range(0, 256, 10): 
        set_led_color(brightness, 0, brightness)
        time.sleep(0.05)
    for brightness in range(255, -1, -10): 
        set_led_color(brightness, 0, brightness)
        time.sleep(0.05)
```

Synchronizing mode:
``` Python  
def sync_effect():
    for i in range(3): 
        set_led_color(0, 255, 0)
        time.sleep(0.2)
        set_led_color(0, 0, 0) 
        time.sleep(0.2)
```

Resting mode：
``` Python  
set_led_color(255, 80, 0)
```


### Physical Components   

For the prototype, I chose a white scarf as the base because it enhances the visibility of the LED lights and creates a diffusive effect on the fabric, making the light patterns more vibrant and evenly distributed.

![physical_component](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/project%202/physical_component.jpg)


### Project Outcome  

The outcome of this project is a responsive, motion-activated lighting system with three distinct modes. The system reacts to user motion in real time, offering an engaging experience through pulsing, flashing, and ambient LED effects. Designed with intuitive gestures and visually patterns, this project demonstrates how IMU sensors and RGB lighting can combine to create interactive solutions for wearable technology.

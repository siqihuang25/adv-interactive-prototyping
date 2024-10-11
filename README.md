### Introduction

My project is an interactive savings jar that utilizes an LED strip and copper tape to visually indicate the jar's open or closed status. The LED strip changes colors based on the lid's position, providing immediate feedback to the user.

![concept sketch](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/sketch.jpg) 

### State Diagram

Initial State: When the savings jar is not in use, it remains in a low-power state, with the LED strip glowing softly in a light blue color. This indicates to the user that the jar is idle and ready for interaction.

Opening the Lid: When the lid is opened, the copper tape makes contact, triggering the LED strip to change to a warm yellow color. This color change signals to the user that the jar is now open and ready for deposits, creating awareness without causing alarm.

Closing the Lid: When the lid is closed, the copper tape disconnects, and the LED fades back to the initial light blue color, indicating that the system has returned to its low-power state.

![state diagram](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/state%20diagram.jpg) 

### Hardware

* M5Stack Atom Lite  
* Digital RGB LED Weatherproof Strip
* Copper Tape
* USB-C Cable
* Alligator Clips

![hardware](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/hardware.jpg)

### Firmware   

RGB Strip Initialization:

``` Python  
rgb_strip = RGB(io=2, n=10, type="SK6812")
```

Initial State (Low Power Mode):

``` Python  
rgb_strip.fill_color(0xADD8E6)
```

Lid Status Detection:

``` Python  
if input_pin.value() == False:
    rgb_strip.fill_color(0xFFFF00)  # Yellow for open lid
else:
    rgb_strip.fill_color(0xADD8E6)  # Light blue for closed lid
```

### Physical Components   

I used a plastic container for the savings jar, with copper tape applied to the rim of the jar and the lid to detect when the lid is opened or closed. This simple, lightweight container can be easily modified for interactive projects.

![physical component](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/physical_component.jpg)

### Project Outcome  

The interactive savings jar responds effectively to the lid being opened and closed. When the lid is opened, the LED turns yellow; when closed, it returns to a soft blue, indicating that the jar is secure and in a low-power state.

![project outcome](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/project_outcome.jpg)

Initially, I intended to incorporate additional states into the design. However, the rapid flashing of the LEDs made it challenging for users to recognize and track the various states. Consequently, I streamlined the system to focus on just two core states. Due to limited supplies, such as sensors or weight detection tools, I was unable to fully implement these advanced features. In the future, integrating more precise sensors could enable the jar to differentiate between various interactions, thereby enhancing both its interactivity and security.

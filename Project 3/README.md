### Introduction

My project is a proximity-based interactive LED scarf system designed to change visual modes dynamically based on the distance between two scarves.

### State Diagram

Initial State: When the system starts or neither scarf detects the other

Close Proximity Mode：When the distance between the two scarves is less than 20 cm

Medium Proximity Mode: When the distance between the two scarves is 20-50cm

Far Proximity Mode:  When the distance between the two scarves is more than 50cm

Lost Connection Mode: When neither scarf can detect the other using ToF or communication modules.

## Hardware

* M5Stack Atom Lite  
* Digital RGB LED Weatherproof Strip
* USB-C Cable
* M5Stack ToF Distance

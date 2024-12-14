### Introduction

My project is a cloud-enabled proximity-based interactive LED scarf system. The scarves change their visual modes based on the distance between them, with data processed and synchronized through a cloud platform.

![sketches](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/Project%203/sketches.png)

### State Diagram

Initial State: When the system starts or neither scarf detects the other

Close Proximity Mode：When the distance between the two scarves is <= 20 cm

Medium Proximity Mode: When the distance between the two scarves is 20-50cm


## Hardware

* M5Stack Atom Lite  
* Digital RGB LED Weatherproof Strip
* USB-C Cable
* M5Stack ToF Distance

## Firmware

Interpolate between multiple colors:
``` Python  
def interpolate_colors(colors, ratio):
    idx = int(ratio * (len(colors) - 1))
    next_idx = min(idx + 1, len(colors) - 1)
    local_ratio = (ratio * (len(colors) - 1)) % 1
    start_color = colors[idx]
    end_color = colors[next_idx]
    r = int(((start_color >> 16) * (1 - local_ratio) + (end_color >> 16) * local_ratio))
    g = int((((start_color >> 8) & 0xFF) * (1 - local_ratio) + ((end_color >> 8) & 0xFF) * local_ratio))
    b = int(((start_color & 0xFF) * (1 - local_ratio) + (end_color & 0xFF) * local_ratio))
    return (r << 16) | (g << 8) | b
```

Receive color feed from Adafrui Io：
``` Python  
def color_feed_callback(data):
    global color
    color_str = data[1].decode()
    print('Received color:', color_str)
    color = get_color_from_hexstr(color_str)

mqtt_client.subscribe(aio_user_name + '/feeds/color', color_feed_callback)
```

Adjust gradient range based on distance：
``` Python  
if distance <= 20:
            colors = [color, scarf_1_color]
        elif distance <= 50:
            mid_color = interpolate_colors([color, scarf_1_color], 0.5)
            colors = [color, mid_color, scarf_1_color]
        else:
            mid_color1 = interpolate_colors([color, scarf_1_color], 0.33)
            mid_color2 = interpolate_colors([color, scarf_1_color], 0.66)
            colors = [color, mid_color1, mid_color2, scarf_1_color]
```


### Project Outcome

Initially, we used Bluetooth to connect two scarves, but we ultimately transitioned to a cloud-based solution, enabling users to fully customize the color and brightness of their scarves to suit their preferences. This shift not enhanced user experience and also expanded the potential for scalable and personalized interactions. While the core functionality is complete and performing well, the animation feature is something I aim to refine in future iterations. Looking ahead, I’m excited to explore the integration of additional sensors, such as heart rate monitors, to incorporate emotional responses and deepen the theme of "connection" through innovative, interactive features.

![project outcome](https://github.com/vanessahuang29/adv-interactive-prototyping/blob/main/Project%203/scarf.jpg)

### Final Video

---
title: "RoboHand"
author: "Akshit Erukulla"
description: "A robotic finger has 2–3 hinged segments moved by servos or tendons, controlled by a microcontroller and powered by a battery."
created_at: "2025-06-26"
---

# June 26th:
I worked on my CAD. I had to really think about how to design the finger. I decided to start off with some cylidners and then processeded to hollow them out, cut them, connect them, then add the plates with holes for a string (kevlar line) to go through all the fingers, so it can pull and curl the fingers.
I planned how I was going to design the whole finger and motion (sideways, and curling motion). I decided to use a string to curl the finger, by making a motor pull the string. For sideways movement, I will just use a servo motor probably.

![CAD Finger](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0a3ebe69d523984b68b492a90954d45204293030_cad_j26.png)

**Total time spent: 1.5h**

# June 27th:
I completely changed my cad and tried to model an actual finger. I found a reference iamge so I worked off based off of that. This took a lot of tiem because I had to also develop parts for the bendable parts fo the finger. I had to use many different shapes and in the images atached, there should be one that shows how many different shapes I had to carefully plan out.

![CAD Finger Part Before](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d1c07f8ec9090210d5a8d6e361ce2323bc493307_cad_before.png)

![CAD Finger Parts Lined Up](https://hc-cdn.hel1.your-objectstorage.com/s/v3/61f96df60791a419fe90df3006d5751112250500_cad_j27.png)

**Total time spent: 3.5h**

# June 28th:
I finished my CAD I think. I addee the hinges, I added the holes/guides for the kevlar string. I also added the holes for where I would connect the finger parts, and designed the tubes I need for that.

![CAD Finger Whole Frontside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/ca22cae002d508cb46458881a8eacebcb9c0355e_cad_j28_pic1.png)

![CAD Finger Whole Backside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/59463f1d8ecd6e6754e5053a6f7db0f88449871a_cad_j28_pic2.png)

**Total time spent: 3.5h**

# June 29th:
I just added the servo motor holder (it took some time designing the holder for the servo motor accurately and also its axle's shape stuff) and the spool I will need to the CAD. For my final CAD file, I will take the stuff apart and put them separate so that the 3D printer can actually properly 3D print stuff.

![CAD Finger Whole](https://hc-cdn.hel1.your-objectstorage.com/s/v3/4f2ae77bd89a0d3aa96313b83e6d795bb50f3154_cad_j29.png)

**Total time spent: 1.5h**

# June 30th:
I designed the schematic for my robot finger/hand. I decided that all I will need is an ESP32-CAM module and a servo motor. So, I added those (it took some time to also add the symbol libraries and footprints too). I also realized I needed to add a capacitor as well. After runnign ERC, I received a few errors, so I fixed the unconnected pins with a No Connect end, and then also added the PWR_FLAGs. I was originally going to design a PCB too, but I realized that since it's just one finger, and also there may be some errors and refinning and testing and stuff, a PCB would take too long to make each time.

![Schematic](https://hc-cdn.hel1.your-objectstorage.com/s/v3/802837c75aa30302b7183fd66e1f129e9aac8e3f_pcb_j30.png)

**Total time spent: 1.5h**

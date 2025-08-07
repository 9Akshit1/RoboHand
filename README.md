# RoboHand
DESCRIPTION: RoboHand is just like how it sounds. It is a robotic hand with five fingers that can mimic real hand movements. It uses small servo motors controlled by a smart camera board to copy gestures like fists or peace signs. The hand can also be controlled manually via a computer or preset motions for easy testing and flexibility.

INSPIRATION: I've always been inspired by how human hands move and wanted to recreate that motion using motors and tendons. Additionally, at the same time, I was learning how to simulate robots in physics based simulations called MuJoCo, which is why I wanted to also actaully build a hand and test my inverse kinematics coding knowledge at it.

# Final CAD
The separate finger files and body files are in ther CAD folder. The full built hand CAD File is called RoboHand.stl in the CAD folder. 

The below five images are each finger's separated pieces. They are all essentially copies of the Middle_Finger.stl file, except they have been scaled to be shorter. 

Also, please note that I can always just add supports before I 3D print, so we do not need to worry about that!

Middle Finger (the original finger):

![Final CAD Middle Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/47549fec8bafb1626f2fa633d8798c469f0eecc3_cad_middle.png)

Thumb Finger (a scaled down version of the middle finger):

![Final CAD Thumb Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d47e26595ff6a854219f9481595280e4a03abd23_cad_thumb.png)

Index Finger (a scaled down version of the middle finger):

![Final CAD Index Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5cedf0068f997ff48cd3f0cf27c2add3f5ba289a_cad_index.png)

Ring Finger (a scaled down version of the middle finger):

![Final CAD Ring Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/1159341951d918dbfab7d8ad09b1596d0c0ad3dc_cad_ring.png)

Pinky Finger (a scaled down version of the middle finger):

![Final CAD Pinky Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/3ad1caff27a0c6759d0816a451dc2e8561a90a3a_cad_pinky.png)

Also, note that for the below hand-body/palm separated image, none of the parts are touching but they are very close to each other. That is just temporary. When I actually 3D print everything, I will separate those parts into different CAD files.

![Final CAD Body Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/7041112042d07831d98d7bf883e41fcbb0f77385_cad_body.png)

This is what the full build hand will look like. I will likely hot glue every piece together. 

![Final CAD Frontside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0eb5953f91e9ba583a2f5a64e0ce6e3ec2b6b9e5_cad_jy2_pic1.png)

![Final CAD Backside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/6cf5f00cecec6dab7e3f775ddf35739472e9989b_cad_jy3.png)

![Final CAD Underside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/b559a07c66fa4c035cc92b1351936754b3420eb1_cad_jy2_pic3.png)

# Final Circuit Schematic
Schematic is called robohand.kicad_sch in the schematic_pcb/robohand folder.

![Final Schematic](https://hc-cdn.hel1.your-objectstorage.com/s/v3/319bd1ee434b18614ffb52b6fccd42de33fba531_schematic_jy2.png)

# Final PCB (I'm not actually gonna use a PCB, I just made this for practice)
Schematic is called robohand.kicad_pcb in the schematic_pcb/robohand folder.

![Final PCB](https://hc-cdn.hel1.your-objectstorage.com/s/v3/e38e3dc7e2b150734c08eded3e18af604725a4f3_pcb_jy2.png)

# Final Firmware Stuff
The firmware software is in the firmware folder, and are called esp32_ver.py (which will be used on the ESP32-CAM board), and pc_ver.py (which can be tested on a PC).

![Camera Tracking UI Full Hand Open](https://hc-cdn.hel1.your-objectstorage.com/s/v3/33b4f0d4d17303a596ea11bbbde2154588fb1819_camera_tracking_full.png)

![Camera Tracking UI Spider Man Pose](https://hc-cdn.hel1.your-objectstorage.com/s/v3/088d54ca0e6f30fa80a4ac7c3bd3eefce8f310bd_camera_tracking_spiderman.png)

## Bill of Materials (BOM)

| Item                             | Quantity | Total Cost (USD) | Description / Part Number                      | Notes                                | Links                             |
|---------------------------------|----------|-------------------|-----------------------------------------------|-------------------------------------|-------------------------|
| **ESP32-CAM module**             | 1        | $9.04 | ESP32-CAM Module                | Main controller + camera             | https://www.aliexpress.com/item/1005006341099716.html?spm=a2g0o.productlist.main.4.10b31f44f3CRYE&algo_pvid=cf5cc23f-74d1-44a8-bcb2-311bc13f1dcc&algo_exp_id=cf5cc23f-74d1-44a8-bcb2-311bc13f1dcc-3&pdp_ext_f=%7B%22order%22%3A%22103%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21CAD%212.83%211.63%21%21%2114.42%218.32%21%402101d9ee17540044723562302eab01%2112000036821212387%21sea%21CA%216438900822%21ABX&curPageLogUid=s9SbCAg5Mvaq&utparam-url=scene%3Asearch%7Cquery_from%3A |
| **ESP32-CAM DEV Board**             | 1        | $2.08 | ESP32-CAM DEV Board                | Needed to actualyl conenct ESP32 and program it            | https://www.aliexpress.com/item/1005006341099716.html?spm=a2g0o.productlist.main.4.10b31f44f3CRYE&algo_pvid=cf5cc23f-74d1-44a8-bcb2-311bc13f1dcc&algo_exp_id=cf5cc23f-74d1-44a8-bcb2-311bc13f1dcc-3&pdp_ext_f=%7B%22order%22%3A%22103%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21CAD%212.83%211.63%21%21%2114.42%218.32%21%402101d9ee17540044723562302eab01%2112000036821212387%21sea%21CA%216438900822%21ABX&curPageLogUid=s9SbCAg5Mvaq&utparam-url=scene%3Asearch%7Cquery_from%3A |
| **MG90S Servo Motor**            | 10        | $20.99 | Metal Gear Micro Servo, 9g                     | Cheapest price servo motor. Need 3 for thumb, because it has that many DOF and each of those are important. We have 4 motors for the lower section's movement of the other fingers. Ideally, I wouldve wanted another 4 more motors so I could control the middle section's movement of the other fingers, but the aliexpress link only allows me to buy 3 more, so I'll need to buy another one on my own later.                      | https://www.aliexpress.com/item/1005008626768357.html?spm=a2g0o.productlist.main.2.7f2015caxNFEhm&aem_p4p_detail=202507311630421114710384897480003208335&algo_pvid=f808fc16-865d-4975-95a1-d6fab4f69bc5&algo_exp_id=f808fc16-865d-4975-95a1-d6fab4f69bc5-1&pdp_ext_f=%7B%22order%22%3A%22317%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21CAD%215.83%211.63%21%21%214.12%211.15%21%402101c59517540046428904607ef048%2112000046009069094%21sea%21CA%216438900822%21ABX&curPageLogUid=JxTQbST0aPKs&utparam-url=scene%3Asearch%7Cquery_from%3A&search_p4p_id=202507311630421114710384897480003208335_1 |
| **Electrolytic Capacitor 1000µF, 10V** | 1        | $3.21 | Radial leaded capacitor                        | Power filtering. The link has 10 pcs but there was no other product that only sold 1 piece and this was the cheapest  | https://www.aliexpress.com/item/33010665515.html?spm=a2g0o.productlist.main.19.5696e336YqdJ1M&algo_pvid=05eaeade-4550-4688-b75d-17b6cb5b207e&algo_exp_id=05eaeade-4550-4688-b75d-17b6cb5b207e-18&pdp_ext_f=%7B%22order%22%3A%2270%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21CAD%214.37%211.63%21%21%213.09%211.15%21%402101ef5e17540057514022423e8084%2167121829359%21sea%21CA%216438900822%21ABX&curPageLogUid=NYzuwQWBHlT4&utparam-url=scene%3Asearch%7Cquery_from%3A |
| **Male/Female Jumper Wires**     | ~15      | N/A| Dupont cables (already owned)                                 | For wiring servos, buttons, ESP32   | N/A |
| **Female Power Adapter DC Barrel to Screw Plug Jack Connector** | 1 | $2.52 | Mr.Geeker 10 Pcs Female Power Adapter DC Barrel to Screw Plug Jack Connector 2.1x5.5mm | Used to connect the power adapter to the ESP32-CAM board but manage the power and GND. The product link was the cheapest deal I could find | https://www.aliexpress.com/item/1005008987005268.html?spm=a2g0o.productlist.main.2.df155998nLKCjG&aem_p4p_detail=202508011402373093864537015840004227846&algo_pvid=96a38800-3a1a-4c03-b19f-4abbd7d5611a&algo_exp_id=96a38800-3a1a-4c03-b19f-4abbd7d5611a-1&pdp_ext_f=%7B%22order%22%3A%2229%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21CAD%213.43%211.63%21%21%2117.48%218.31%21%402101e9ec17540821576896587efa3e%2112000047469895587%21sea%21CA%216438900822%21ABX&curPageLogUid=bBj4EJuoberQ&utparam-url=scene%3Asearch%7Cquery_from%3A&search_p4p_id=202508011402373093864537015840004227846_1 |
| **EMG Sensors** | SEN-13723 RoHS MyoWare | 3 | $90.00 | https://www.alibaba.com/product-detail/SpotMyoWare-Muscle-Sensor-SEN-13723-Muscles_1601406726720.html?spm=a2700.galleryofferlist.normal_offer.d_title.52e313a0BHVrsO | Muscle activity sensors. These are one of the best quality sensors suitable for research projects such as this and are also the cheapest deal I found everywhere! I need 3 because I'm doing a full hand, meaning there are multiple muscles to look at and analyze and align and everything. |

**BOM Cost:** $127.84 USD ≈ $174.17 CAD            (I made it MUCH MUCH cheaper than what's shown on the form submission!)

**Shipping:** $0.00 USD ≈ $0.00 CAD     --- Everything is FREE SHIPPING becuase this will be my frist ever order on Aliexpress

**Taxes (in  Ontario, Canada, it's 13%):** $16.62 USD ≈ $22.64 CAD

**Total Cost:** $144.46 USD ≈ $196.81 CAD

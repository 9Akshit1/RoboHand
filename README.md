# RoboHand
DESCRIPTION: RoboHand is just like how it sounds. It is a robotic hand with five fingers that can mimic real hand movements. It uses small servo motors controlled by a smart camera board to copy gestures like fists or peace signs. The hand can also be controlled manually via a computer or preset motions for easy testing and flexibility.

INSPIRATION: I've always been inspired by how human hands move and wanted to recreate that motion using motors and tendons. Additionally, at the same time, I was learning how to simulate robots in physics based simulations called MuJoCo, which is why I wanted to also actaully build a hand and test my inverse kinematics coding knowledge at it.

# Final CAD
The separate finger files and body files are in ther CAD folder. The full built hand CAD File is called RoboHand.stl in the CAD folder. 

The below five images are each finger's separated pieces. They are all essentially copies of the Middle_Finger.stl file, except they have been scaled to be shorter. The images below might be slightly different from the current CAD files because I may have noticed a few things to fix, but it's only slight changes.
Also, please note that I can always just add supports before I 3D print, so we do not need to worry about that!
![Final CAD Thumb Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d47e26595ff6a854219f9481595280e4a03abd23_cad_thumb.png)

![Final CAD Middle Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/47549fec8bafb1626f2fa633d8798c469f0eecc3_cad_middle.png)

![Final CAD Index Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5cedf0068f997ff48cd3f0cf27c2add3f5ba289a_cad_index.png)

![Final CAD Ring Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/1159341951d918dbfab7d8ad09b1596d0c0ad3dc_cad_ring.png)

![Final CAD Pinky Finger Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/3ad1caff27a0c6759d0816a451dc2e8561a90a3a_cad_pinky.png)

Also, note that for the body separated image, none of the parts are touching but they are very close to each other. That is just temporary. When I actually 3D print everything, I will separate those parts into different CAD files.
![Final CAD Body Separated](https://hc-cdn.hel1.your-objectstorage.com/s/v3/7041112042d07831d98d7bf883e41fcbb0f77385_cad_body.png)

This is what the full build hand will look like. I will likely hot glue every piece together. 
![Final CAD Frontside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0eb5953f91e9ba583a2f5a64e0ce6e3ec2b6b9e5_cad_jy2_pic1.png)

![Final CAD Backside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/6cf5f00cecec6dab7e3f775ddf35739472e9989b_cad_jy3.png)

![Final CAD Underside](https://hc-cdn.hel1.your-objectstorage.com/s/v3/b559a07c66fa4c035cc92b1351936754b3420eb1_cad_jy2_pic3.png)

# Final Circuit Schematic
Schematic is called robohand.kicad_sch in the schematic_pcb/robohand folder.

![Final Schematic](https://hc-cdn.hel1.your-objectstorage.com/s/v3/319bd1ee434b18614ffb52b6fccd42de33fba531_schematic_jy2.png)

# Final PCB
Schematic is called robohand.kicad_pcb in the schematic_pcb/robohand folder.

![Final PCB](https://hc-cdn.hel1.your-objectstorage.com/s/v3/19efd4e19a08c81d7d72a219a6a06c1f867fb6a9_pcb_jy2.png)

# Final Firmware Stuff
The firmware software is in the firmware folder, and are called esp32_ver.py (which will be used on the ESP32-CAM board), and pc_ver.py (which can be tested on a PC).

![Camera Tracking UI Full Hand Open](https://hc-cdn.hel1.your-objectstorage.com/s/v3/33b4f0d4d17303a596ea11bbbde2154588fb1819_camera_tracking_full.png)

![Camera Tracking UI Spider Man Pose](https://hc-cdn.hel1.your-objectstorage.com/s/v3/088d54ca0e6f30fa80a4ac7c3bd3eefce8f310bd_camera_tracking_spiderman.png)

## Bill of Materials (BOM)

| Item                             | Quantity | Total Cost (USD) | Description / Part Number                      | Notes                                | Links                             |
|---------------------------------|----------|-------------------|-----------------------------------------------|-------------------------------------|-------------------------|
| **ESP32-CAM module**             | 1        | $18.72 | AI-Thinker ESP32-CAM Dev Board                | Main controller + camera             | https://www.amazon.ca/YTHYTHYTH-ESP32-CAM-Camera-Module-Development/dp/B0CPYHC78H/ref=sr_1_12?crid=3R6YW95QXMOY0&dib=eyJ2IjoiMSJ9.p-7w9ePEFV8IlVtRqh8K-qPFy3CIjEz1G89o405BmgjVNBJgpYSemxviNOA83UIRs3iBblZg1A37S3bUkd1h8TGR6w6Rw_ihX-QSSlSFAQNpK_PQIXiOHW-XynXMMCn6Cphgg7CiChYX7GfHgCmi-OCHkh8HEAZhzp31Z19n4RzhynYaf_vGAGf4_bXgiIoJphSv-oJVRquPAmfrJLaKYUAgUtL3mWFFXi61eqMGpwZ9kPWA3_OVvuAqskSyFnPG9hpguHwnTXcAzDdNchyvvns_PEQCWOqCKdrBdSN4N3k.CodZzIIIr3v_uHrhYZ5CobgXKMWTFr0goLA8PYGQ7Qw&dib_tag=se&keywords=ESP32-CAM+module&qid=1751678624&sprefix=esp32-cam+module%2Caps%2C162&sr=8-12 |
| **MG90S Servo Motor**            | 5        | $13.84 | Metal Gear Micro Servo, 9g                     | One per finger                      | https://www.amazon.ca/MG90S-MG-90S-Servo-Motor-Micro/dp/B0C6XSLBHT?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=AW9T8AN8WY1PG& |
| **Pushbutton Switch (NO, SPST)**| 3        | $7.35 | Mini tactile pushbutton switch                 | For mode selection buttons. The link is the cheapest one (in terms of price per piece) I could find including the shipping (since its in Canada where I live)            | https://www.amazon.ca/uxcell-6x6x5mm-Terminals-Button-Switch/dp/B07JM27QJC/ref=sr_1_26_sspa?crid=8OVUDT7K975T&dib=eyJ2IjoiMSJ9.qd83T_Ya94qiqPvR9N-A8lTnp-ChpK7iVXoOqFizaOYkTLgfciaQnGeunpBFzYqQX6Mz8pec8gj78s5yyJUivwUu8beh-YY6NgmqU0qTIh7H7d4dwIXUj9IYcSJc8dQctK7Q5GRhBoI4tRm8tr2Dyp1jTi2Pl5lIvp_rfZ0MxeTU7dboaS4toChNk5tH0QEEyt3me4I_LALUOdg-otp-RpdY7VQUh1F-u51FCgbxqAxsoqU9TYhK9vvD0bTB7it3GxyY6ueHMpYpukeAkqJRIeMNvkExOlgjpgvvFYwWzbI.cM575hV-KyB_pEZ9SYoIAl4u9f3eIMTUE_Vdm6QYL7Y&dib_tag=se&keywords=6+x+6mm+x+5mm+Momentary+Tactile+Tact+Push+Button+Switch&qid=1751494932&s=industrial&sprefix=6+x+6mm+x+5mm+momentary+tactile+tact+push+button+switch%2Cindustrial%2C79&sr=1-26-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9idGY&psc=1 |
| **Electrolytic Capacitor 1000µF, 10V** | 1        | $7.35 | Radial leaded capacitor                        | Power smoothing for servo supply. The cheapest version is in the link (20 pieces), because buying singular ones are extremely expensive due to shipping     | https://www.amazon.ca/uxcell-1000uF-Radial-Electrolytic-Capacitor/dp/B016EK6H9M?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A24JGA3DO5B17D |
| **USB 5V 3A DC–DC Converter**        | 1        | $8.24 | USB Power Adapter | Powers servos and ESP32               | https://www.amazon.ca/G120503-Converter-Waterproof-Convertor-Navigation/dp/B0D2RGT8SW/ref=sr_1_30?crid=3T02RXA869K2K&dib=eyJ2IjoiMSJ9.RCqtb0XsfR_6_BGOPxv0xWeBKKqKtnA5YvT0M9m1xofv7K_K81XqPc39T67mAic-7o_Mgdl4rDtqRbcywQ7ishHXHlwN9-V2Wbz-5HUF8VHUmi0ZV0hvfWRxwXg09hQFzQIxY3o3idbtoLgfVIkzow7oIurvo5-8-5IV5KNGWjgpP1az9SZs5MDdJXPeA0gDSqj7FAeDuyTWKRGdxbOHJOx6yIQAXTlXr5vA6O0wC8AxmhEGy388txB9bzePne0PEX0zRRkToGXiWfvKPkqoFyTrPhQqY6X7ePLvBipUdno.FfV4lEZFD8gfKbJGWBc0-1i2fj1XBKNsEN2J3lpFW_0&dib_tag=se&keywords=USB+5%E2%80%AFV%E2%80%AF3%E2%80%AFA+DC%E2%80%93DC+Converter&qid=1751494719&sprefix=usb+5+v+3+a+dc+dc+converter%2Caps%2C140&sr=8-30 |
| **Male/Female Jumper Wires**     | ~15      | Already Owned | Dupont cables                                 | For wiring servos, buttons, ESP32   | N/A |
| **USB to Serial Adapter (FTDI)** | 1        | $6.48 | For programming ESP32-CAM                      | ESP32-CAM has built-in USB, but I do not have this, which is why I need it | https://www.amazon.ca/Adapter-Performance-Communication-Devices-Plastic/dp/B0F7QXZ8RD/ref=sr_1_9?crid=13LQDG99MDTY5&dib=eyJ2IjoiMSJ9.DyyY_BaJKhhtwx9FpQgni-wzcTRbKnWTOOqX5PUKcIVWNo0ELQH4m9f6YVSOlCodje7pcUqgyeh3n9kqVpRkOMv2VVW51wU8_7Bingex-otlIUPB4I6KIclMSUeXH1NM30BfGkiwFLpI7YH_FUapqx2DMAYS_XrC8-wUhupkJzGqrKwWO5hlY4iFboHxqZO8x5IP2CPOVCSM6fqmBMTDN9vuIEsDNV0fmVx2XZLS0cx4DLTM7QbSUv1VwmlsH41OpJ4mfnqlx0t7gyZsXwwsFiUz6G6ukTS3uNfFXYIsKMY.3P1SY_BjfWnqM2rl_S7ds6JBB8qjUlIBxBBDOMbnvAo&dib_tag=se&keywords=**USB+to+Serial+Adapter+%28FTDI%29**&qid=1751495070&sprefix=usb+to+serial+adapter+ftdi+%2Caps%2C147&sr=8-9 |
| **3D Printed Parts (CAD)**	| Varies   | $5.00 - $20.00    | Finger joints, palm base, mounts (~75g PLA)    |  Varies by the estimated filament cost and the number of trials of testing | N/A |
| **3 Pin JST-XH Connector (20 pieces)** | 1 | $6.78 | 20 Sets Pack Micro JST 1.25MM 3 Pin Male Female Connector Plug with Wires Cables | Need this to coneect the servo motors and the V+s and the GNDs | https://www.amazon.ca/1-25MM-Female-Connector-Cables-Circuit/dp/B0DDJSTVWX/ref=sr_1_16?crid=2I8LPHQTNL9T5&dib=eyJ2IjoiMSJ9.a0Ks31eMb2jXaw3wDK6PcIVx4FeHxdih-UCEZ3CKKWydOtoVfIjiLRPHqy5p7bDT3k51PceWSRUK4qgAJl1B-kDUmS52fSxDNLsYXKgoXJU8sWQqAg7Z7e6ip-FGHc5XWVLx7w0HWCKy9QAOXn0mXOivHXjJhXMDZuMN8UxmyaKcqBFb4yXaK7XjvBtmJ52ZlnCibS2oyG1u9rP8r8RTmdHRmpf3vA3r8UmbYcrW3q2DsTc3Plp2vZYxlroxycFmJxbKZkmnTuBbF5hHoVtzIbTY-DPRZ7-jqW7L1bobxmg.ZgdPgBnRNN4L9o5P_RviG2VtrsPwxMUokMbO8ADUnnE&dib_tag=se&keywords=3%2BPin%2BJST-XH%2BConnector%2B(5%2Bpack)&qid=1751550453&s=industrial&sprefix=3%2Bpin%2Bjst-xh%2Bconnector%2B5%2Bpack%2B%2Cindustrial%2C120&sr=1-16&th=1 |
| **3‑Pin Header (2.54 mm)** | 1 | $5.14 | Chanzon Pin Header Strip for Arduino Gpio 3 pin x 50pcs Female Headers Pins Straight Single Row Gold Plated Pitch 2.54mm | Need this to connect the servo motors and the V+s and the GNDs. The link is the best deal even though it has 50pcs. | https://www.amazon.ca/Chanzon-Straight-Connector-Breadboard-Electronic/dp/B09MYMD4YS/ref=sr_1_6?dib=eyJ2IjoiMSJ9.mDbMAvzdM6g4dBzmQLGDYp0rm8V6ylAvJzs7rYeFPJiQnEai4Hut0iD4Kza4cwOGX8O1uJbzuhTmmtLasfeflTAKGH4LVbg4qxSevtJZacJ7vvxI38qY1Es-2gSAvIRlqmiiFlhPpBKLRmPCOFMg748H1IoGyEBx4xMyGaUlXOsuQ2Eg-vwqFopRaahvGXdz1NO4Tss86FAdDCwIbZ4lbdGqQMsYaR1qwsGRuxsj57ye1-B9VHJtDNnkyUG9pBPljYHlZxmnLOSJu6ClohOeoPD_raN_eTp_yiKCIo2SddY.z78eETkofenIQQpZtlKoPOrTk4jGViAwh4BvKMjlzKg&dib_tag=se&keywords=3%E2%80%91Pin+2.54%E2%80%AFmm+Pin+Header&qid=1751678084&sr=8-6 |
| **Female Power Adapter DC Barrel to Screw Plug Jack Connector** | 1 | $7.36 | Mr.Geeker 10 Pcs Female Power Adapter DC Barrel to Screw Plug Jack Connector 2.1x5.5mm | Used to connect the power adapter to the ESP32-CAM board but manage the power and GND. The product link was the cheapest deal I could find | https://www.amazon.ca/dp/B00NXGVWIM |

**BOM Cost (with 3D CAD using the average of the range which is $12.5):** $93.76 USD ≈ $130.78 CAD

**Shipping (from the links the largest shipping fee):** $5.88 USD ≈ $8 CAD 

**Subtotal:** $99.64 USD ≈ $135.54 CAD 

**Taxes (in  Ontario, Canada, it's 13%) are together:** $12.95 USD ≈ $17.62 CAD

**Total Cost:** $112.59 USD ≈ $153.16 CAD

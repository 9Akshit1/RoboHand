"""
ESP32-CAM 5-Finger Robotic Hand Controller
MicroPython code for ESP32-CAM development board

Hardware Setup:
- 5x MG90S servo motors on GPIO2, GPIO4, GPIO13, GPIO14, GPIO15
- 3x pushbuttons on GPIO12, GPIO16, GPIO0 (with internal pull-ups)
- ESP32-CAM onboard camera for Mode 3
"""

import machine
import time
import json
from machine import Pin, PWM
import sys

# Configuration
SERVO_PINS = [2, 4, 13, 14, 15]  # GPIO pins for 5 servos (thumb to pinky)
BUTTON_PINS = [12, 16, 0]        # GPIO pins for 3 mode buttons
SERVO_FREQ = 50                  # 50Hz for servo control (20ms period)

# Servo angle to duty cycle mapping (for 0-180 degrees)
MIN_DUTY = 26   # ~0.5ms pulse width (0 degrees)
MAX_DUTY = 128  # ~2.5ms pulse width (180 degrees)

# Gesture presets (finger angles in degrees)
GESTURES = {
    'fist': [0, 0, 0, 0, 0],           # All fingers curled
    'open': [180, 180, 180, 180, 180], # All fingers straight
    'peace': [0, 180, 180, 0, 0],      # Index and middle straight
    'thumbs_up': [180, 0, 0, 0, 0],    # Only thumb up
    'point': [0, 180, 0, 0, 0],        # Only index finger
    'rock': [0, 180, 0, 0, 180]        # Rock and roll gesture
}

class ServoController:
    """Controls individual servo motors with angle mapping"""
    
    def __init__(self, pin_num, name):
        self.pin_num = pin_num
        self.name = name
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(SERVO_FREQ)
        self.current_angle = 90  # Start at middle position
        self.set_angle(90)
    
    def angle_to_duty(self, angle):
        """Convert angle (0-180) to PWM duty cycle"""
        angle = max(0, min(180, angle))  # Clamp to valid range
        duty = MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)
        return int(duty)
    
    def set_angle(self, angle):
        """Set servo to specific angle"""
        self.current_angle = angle
        duty = self.angle_to_duty(angle)
        self.pwm.duty(duty)
        print(f"Servo {self.name} (GPIO{self.pin_num}): {angle}° (duty: {duty})")
    
    def get_angle(self):
        """Get current servo angle"""
        return self.current_angle

class ButtonHandler:
    """Handles button input with debouncing"""
    
    def __init__(self, pin_num, callback, name):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.callback = callback
        self.name = name
        self.last_state = 1
        self.last_time = 0
        self.debounce_time = 200  # 200ms debounce
    
    def check(self):
        """Check button state and call callback if pressed"""
        current_state = self.pin.value()
        current_time = time.ticks_ms()
        
        # Button pressed (falling edge with debounce)
        if (self.last_state == 1 and current_state == 0 and 
            time.ticks_diff(current_time, self.last_time) > self.debounce_time):
            print(f"Button {self.name} pressed!")
            self.callback()
            self.last_time = current_time
        
        self.last_state = current_state

class RoboticHand:
    """Main controller for the 5-finger robotic hand"""
    
    def __init__(self):
        self.mode = 0  # 0=Serial, 1=Gesture, 2=Camera
        self.mode_names = ["Serial Control", "Preset Gesture", "Camera Mimic"]
        
        # Initialize servos
        self.servos = []
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        for i, pin in enumerate(SERVO_PINS):
            servo = ServoController(pin, finger_names[i])
            self.servos.append(servo)
        
        # Initialize buttons
        self.buttons = [
            ButtonHandler(BUTTON_PINS[0], lambda: self.set_mode(0), "A"),
            ButtonHandler(BUTTON_PINS[1], lambda: self.set_mode(1), "B"),
            ButtonHandler(BUTTON_PINS[2], lambda: self.set_mode(2), "C")
        ]
        
        print("=== 5-Finger Robotic Hand Initialized ===")
        print(f"Current mode: {self.mode_names[self.mode]}")
        self.print_help()
    
    def set_mode(self, new_mode):
        """Switch operating mode"""
        if new_mode != self.mode:
            self.mode = new_mode
            print(f"\n*** MODE CHANGED TO: {self.mode_names[self.mode]} ***")
            self.print_help()
    
    def print_help(self):
        """Print help for current mode"""
        print("\n--- Available Commands ---")
        if self.mode == 0:  # Serial Control
            print("SET <finger> <angle>  - Set finger angle (0-4, 0-180°)")
            print("GET <finger>          - Get finger angle")
            print("Example: SET 0 90")
        elif self.mode == 1:  # Gesture Mode
            print("GESTURE <name>        - Execute preset gesture")
            print("LIST                  - List available gestures")
            print(f"Available gestures: {list(GESTURES.keys())}")
        elif self.mode == 2:  # Camera Mode
            print("MIMIC <angles>        - Set all fingers from camera data")
            print("CAMERA               - Start camera mimic mode")
            print("Example: MIMIC 90,45,135,60,120")
        print("Buttons: A=Serial, B=Gesture, C=Camera")
        print("----------------------------")
    
    def set_finger_angle(self, finger_index, angle):
        """Set individual finger angle"""
        if 0 <= finger_index < len(self.servos):
            self.servos[finger_index].set_angle(angle)
            return True
        return False
    
    def get_finger_angle(self, finger_index):
        """Get individual finger angle"""
        if 0 <= finger_index < len(self.servos):
            return self.servos[finger_index].get_angle()
        return None
    
    def set_all_fingers(self, angles):
        """Set all finger angles at once"""
        if len(angles) == len(self.servos):
            for i, angle in enumerate(angles):
                self.set_finger_angle(i, angle)
            return True
        return False
    
    def execute_gesture(self, gesture_name):
        """Execute a preset gesture"""
        if gesture_name in GESTURES:
            angles = GESTURES[gesture_name]
            print(f"Executing gesture: {gesture_name}")
            self.set_all_fingers(angles)
            return True
        return False
    
    def process_serial_command(self, command):
        """Process commands from serial interface"""
        try:
            parts = command.strip().upper().split()
            if not parts:
                return
            
            cmd = parts[0]
            
            if self.mode == 0:  # Serial Control Mode
                if cmd == "SET" and len(parts) == 3:
                    finger = int(parts[1])
                    angle = int(parts[2])
                    if self.set_finger_angle(finger, angle):
                        print(f"OK: Finger {finger} set to {angle}°")
                    else:
                        print(f"ERROR: Invalid finger index {finger}")
                
                elif cmd == "GET" and len(parts) == 2:
                    finger = int(parts[1])
                    angle = self.get_finger_angle(finger)
                    if angle is not None:
                        print(f"Finger {finger}: {angle}°")
                    else:
                        print(f"ERROR: Invalid finger index {finger}")
                
                else:
                    print("ERROR: Invalid command for Serial mode")
            
            elif self.mode == 1:  # Gesture Mode
                if cmd == "GESTURE" and len(parts) == 2:
                    gesture = parts[1].lower()
                    if self.execute_gesture(gesture):
                        print(f"OK: Executed gesture '{gesture}'")
                    else:
                        print(f"ERROR: Unknown gesture '{gesture}'")
                
                elif cmd == "LIST":
                    print(f"Available gestures: {list(GESTURES.keys())}")
                
                else:
                    print("ERROR: Invalid command for Gesture mode")
            
            elif self.mode == 2:  # Camera Mode
                if cmd == "MIMIC" and len(parts) == 2:
                    try:
                        angles = [int(x) for x in parts[1].split(',')]
                        if self.set_all_fingers(angles):
                            print(f"OK: Mimicking angles {angles}")
                        else:
                            print(f"ERROR: Need exactly 5 angles, got {len(angles)}")
                    except ValueError:
                        print("ERROR: Invalid angle format")
                
                elif cmd == "CAMERA":
                    print("Camera mimic mode active - send MIMIC commands")
                
                else:
                    print("ERROR: Invalid command for Camera mode")
            
            else:
                print("ERROR: Unknown mode")
        
        except (ValueError, IndexError) as e:
            print(f"ERROR: Command parsing failed - {e}")
    
    def run(self):
        """Main program loop"""
        print("\n=== Robotic Hand Controller Running ===")
        
        while True:
            try:
                # Check buttons
                for button in self.buttons:
                    button.check()
                
                # Check for serial input (non-blocking)
                if sys.stdin in machine.select.select([sys.stdin], [], [], 0)[0]:
                    command = input().strip()
                    if command:
                        self.process_serial_command(command)
                
                # Small delay to prevent excessive CPU usage
                time.sleep_ms(10)
                
            except KeyboardInterrupt:
                print("\n=== Shutting down ===")
                # Return servos to neutral position
                self.set_all_fingers([90, 90, 90, 90, 90])
                break
            except Exception as e:
                print(f"ERROR: {e}")
                time.sleep(1)

# Main execution
if __name__ == "__main__":
    try:
        hand = RoboticHand()
        hand.run()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        # Emergency stop - set all servos to safe position
        for pin in SERVO_PINS:
            try:
                pwm = PWM(Pin(pin))
                pwm.freq(50)
                pwm.duty(77)  # 90 degrees
            except:
                pass
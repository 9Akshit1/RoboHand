"""
PC-Side Robotic Hand Simulator and Testing Program
Simulates ESP32-CAM behavior and provides MediaPipe hand tracking

Features:
- Simulates ESP32 servo control logic
- Serial communication testing
- MediaPipe hand gesture detection
- Interactive testing interface
- Visual servo position display
"""

import time
import threading
import random
import json
import sys
from typing import Dict, List, Optional
import queue

# Optional imports for advanced features
try:
    import cv2
    import mediapipe as mp
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("OpenCV/MediaPipe not available. Camera features disabled.")

try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("PySerial not available. Real hardware communication disabled.")

class ServoSimulator:
    """Simulates an MG90S servo motor"""
    
    def __init__(self, pin_num: int, name: str):
        self.pin_num = pin_num
        self.name = name
        self.current_angle = 90  # Start at middle position
        self.target_angle = 90
        self.moving = False
        self.move_speed = 180  # degrees per second
        self.last_update = time.time()
    
    def set_angle(self, angle: int):
        """Set target angle for servo"""
        angle = max(0, min(180, angle))  # Clamp to valid range
        self.target_angle = angle
        self.moving = (self.current_angle != self.target_angle)
        print(f"🔧 Servo {self.name} (GPIO{self.pin_num}): Target {angle}°")
    
    def update(self):
        """Update servo position (simulate movement)"""
        if not self.moving:
            return
        
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Calculate movement
        max_move = self.move_speed * dt
        diff = self.target_angle - self.current_angle
        
        if abs(diff) <= max_move:
            self.current_angle = self.target_angle
            self.moving = False
            print(f"✅ Servo {self.name}: Reached {self.current_angle}°")
        else:
            move_amount = max_move if diff > 0 else -max_move
            self.current_angle += move_amount
    
    def get_angle(self) -> int:
        """Get current servo angle"""
        return int(self.current_angle)
    
    def is_moving(self) -> bool:
        """Check if servo is currently moving"""
        return self.moving

class HandGestureDetector:
    """MediaPipe-based hand gesture detection"""
    
    def __init__(self):
        if not OPENCV_AVAILABLE:
            self.enabled = False
            return
        
        self.enabled = True
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = None
    
    def start_camera(self):
        """Start camera capture"""
        if not self.enabled:
            return False
        
        self.cap = cv2.VideoCapture(0)
        return self.cap.isOpened()
    
    def stop_camera(self):
        """Stop camera capture"""
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
    
    def detect_hand_angles(self) -> Optional[List[int]]:
        """Detect hand and return finger angles"""
        if not self.enabled or not self.cap:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Flip horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Calculate finger angles (simplified)
                angles = self.calculate_finger_angles(hand_landmarks)
                
                # Display angles on frame
                cv2.putText(frame, f"Angles: {angles}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('Hand Tracking', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return None
                
                return angles
        
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None
        
        return None
    
    def calculate_finger_angles(self, landmarks) -> List[int]:
        """Calculate finger angles from landmarks (simplified)"""
        # This is a simplified calculation
        # In reality, you'd use more complex 3D calculations
        
        # Finger tip and base landmarks
        tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        base_ids = [2, 5, 9, 13, 17]  # Finger bases
        
        angles = []
        for tip_id, base_id in zip(tip_ids, base_ids):
            tip = landmarks.landmark[tip_id]
            base = landmarks.landmark[base_id]
            
            # Simple angle calculation based on Y difference
            y_diff = abs(tip.y - base.y)
            # Map to servo angle (0-180)
            angle = int(y_diff * 180)
            angle = max(0, min(180, angle))
            angles.append(angle)
        
        return angles

class RoboticHandSimulator:
    """Main simulator for the robotic hand system"""
    
    def __init__(self):
        self.mode = 0  # 0=Serial, 1=Gesture, 2=Camera
        self.mode_names = ["Serial Control", "Preset Gesture", "Camera Mimic"]
        
        # Initialize servo simulators
        self.servos = []
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        servo_pins = [2, 4, 13, 14, 15]
        
        for i, (pin, name) in enumerate(zip(servo_pins, finger_names)):
            servo = ServoSimulator(pin, name)
            self.servos.append(servo)
        
        # Gesture presets
        self.gestures = {
            'fist': [0, 0, 0, 0, 0],
            'open': [180, 180, 180, 180, 180],
            'peace': [0, 180, 180, 0, 0],
            'thumbs_up': [180, 0, 0, 0, 0],
            'point': [0, 180, 0, 0, 0],
            'rock': [0, 180, 0, 0, 180]
        }
        
        # Serial communication
        self.serial_port = None
        self.serial_connected = False
        
        # Camera detector
        self.camera_detector = HandGestureDetector()
        self.camera_active = False
        
        # Command queue for threading
        self.command_queue = queue.Queue()
        
        print("🤖 === Robotic Hand Simulator Initialized ===")
        print(f"Current mode: {self.mode_names[self.mode]}")
        self.print_help()
    
    def print_help(self):
        """Print available commands"""
        print("\n--- Available Commands ---")
        print("mode <0|1|2>          - Switch mode (0=Serial, 1=Gesture, 2=Camera)")
        print("connect               - Connect to real ESP32 via serial")
        print("disconnect            - Disconnect from ESP32")
        print("status                - Show system status")
        print("visual                - Show visual servo positions")
        
        if self.mode == 0:  # Serial Control
            print("set <finger> <angle>  - Set finger angle (0-4, 0-180°)")
            print("get <finger>          - Get finger angle")
        elif self.mode == 1:  # Gesture Mode
            print("gesture <name>        - Execute preset gesture")
            print("list                  - List available gestures")
        elif self.mode == 2:  # Camera Mode
            print("camera start          - Start camera hand tracking")
            print("camera stop           - Stop camera hand tracking")
            print("mimic <angles>        - Manually set angles (comma-separated)")
        
        print("quit                  - Exit simulator")
        print("----------------------------")
    
    def connect_serial(self) -> bool:
        """Connect to ESP32 via serial"""
        if not SERIAL_AVAILABLE:
            print("❌ PySerial not available")
            return False
        
        # List available ports
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("❌ No serial ports found")
            return False
        
        print("🔍 Available serial ports:")
        for i, port in enumerate(ports):
            print(f"  {i}: {port.device} - {port.description}")
        
        try:
            port_idx = int(input("Select port (number): "))
            selected_port = ports[port_idx].device
            
            self.serial_port = serial.Serial(selected_port, 115200, timeout=1)
            self.serial_connected = True
            print(f"✅ Connected to {selected_port}")
            
            # Start serial communication thread
            threading.Thread(target=self.serial_communication_thread, daemon=True).start()
            return True
            
        except (ValueError, IndexError, serial.SerialException) as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect_serial(self):
        """Disconnect from ESP32"""
        if self.serial_port:
            self.serial_connected = False
            self.serial_port.close()
            self.serial_port = None
            print("🔌 Disconnected from ESP32")
    
    def serial_communication_thread(self):
        """Handle serial communication in separate thread"""
        while self.serial_connected and self.serial_port:
            try:
                # Send queued commands
                try:
                    command = self.command_queue.get_nowait()
                    self.serial_port.write(f"{command}\n".encode())
                    print(f"📤 Sent: {command}")
                except queue.Empty:
                    pass
                
                # Read responses
                if self.serial_port.in_waiting > 0:
                    response = self.serial_port.readline().decode().strip()
                    if response:
                        print(f"📥 ESP32: {response}")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ Serial communication error: {e}")
                break
    
    def send_command_to_esp32(self, command: str):
        """Send command to ESP32 if connected"""
        if self.serial_connected:
            self.command_queue.put(command)
        else:
            print("⚠️ Not connected to ESP32 - simulating locally")
            self.process_command_locally(command)
    
    def process_command_locally(self, command: str):
        """Process command in simulator"""
        parts = command.strip().upper().split()
        if not parts:
            return
        
        cmd = parts[0]
        
        try:
            if cmd == "SET" and len(parts) == 3:
                finger = int(parts[1])
                angle = int(parts[2])
                if 0 <= finger < len(self.servos):
                    self.servos[finger].set_angle(angle)
                    print(f"✅ Finger {finger} set to {angle}°")
                else:
                    print(f"❌ Invalid finger index {finger}")
            
            elif cmd == "GET" and len(parts) == 2:
                finger = int(parts[1])
                if 0 <= finger < len(self.servos):
                    angle = self.servos[finger].get_angle()
                    print(f"📍 Finger {finger}: {angle}°")
                else:
                    print(f"❌ Invalid finger index {finger}")
            
            elif cmd == "GESTURE" and len(parts) == 2:
                gesture = parts[1].lower()
                if gesture in self.gestures:
                    angles = self.gestures[gesture]
                    for i, angle in enumerate(angles):
                        self.servos[i].set_angle(angle)
                    print(f"✅ Executed gesture '{gesture}'")
                else:
                    print(f"❌ Unknown gesture '{gesture}'")
            
            elif cmd == "MIMIC" and len(parts) == 2:
                angles = [int(x) for x in parts[1].split(',')]
                if len(angles) == 5:
                    for i, angle in enumerate(angles):
                        self.servos[i].set_angle(angle)
                    print(f"✅ Mimicking angles {angles}")
                else:
                    print(f"❌ Need exactly 5 angles, got {len(angles)}")
            
        except (ValueError, IndexError) as e:
            print(f"❌ Command error: {e}")
    
    def show_visual_status(self):
        """Show visual representation of servo positions"""
        print("\n🎯 === Servo Positions ===")
        finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        
        for i, (servo, name) in enumerate(zip(self.servos, finger_names)):
            angle = servo.get_angle()
            # Create visual bar (0-180° mapped to 0-20 chars)
            bar_length = int((angle / 180) * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            status = "🔄" if servo.is_moving() else "✅"
            print(f"{name:>6}: {status} {bar} {angle:>3}°")
        
        print("=" * 35)
    
    def start_camera_tracking(self):
        """Start camera-based hand tracking"""
        if not self.camera_detector.enabled:
            print("❌ Camera/MediaPipe not available")
            return
        
        if not self.camera_detector.start_camera():
            print("❌ Failed to start camera")
            return
        
        print("📹 Camera tracking started. Press 'q' in camera window to stop.")
        self.camera_active = True
        
        # Camera tracking loop
        def camera_loop():
            while self.camera_active:
                angles = self.camera_detector.detect_hand_angles()
                if angles:
                    # Send mimic command
                    angle_str = ','.join(map(str, angles))
                    self.send_command_to_esp32(f"MIMIC {angle_str}")
                time.sleep(0.1)
        
        threading.Thread(target=camera_loop, daemon=True).start()
    
    def stop_camera_tracking(self):
        """Stop camera tracking"""
        self.camera_active = False
        self.camera_detector.stop_camera()
        print("📹 Camera tracking stopped")
    
    def update_servos(self):
        """Update all servo positions"""
        for servo in self.servos:
            servo.update()
    
    def run_interactive(self):
        """Run interactive command interface"""
        print("\n🚀 === Interactive Mode Started ===")
        print("Type 'help' for commands, 'quit' to exit")
        
        # Start servo update thread
        def servo_update_thread():
            while True:
                self.update_servos()
                time.sleep(0.05)  # 20 FPS update
        
        threading.Thread(target=servo_update_thread, daemon=True).start()
        
        while True:
            try:
                command = input("\n🤖 > ").strip().lower()
                
                if command in ['quit', 'exit']:
                    break
                elif command == 'help':
                    self.print_help()
                elif command.startswith('mode '):
                    try:
                        new_mode = int(command.split()[1])
                        if 0 <= new_mode <= 2:
                            self.mode = new_mode
                            print(f"🔄 Mode changed to: {self.mode_names[self.mode]}")
                            self.print_help()
                        else:
                            print("❌ Invalid mode. Use 0, 1, or 2")
                    except (ValueError, IndexError):
                        print("❌ Invalid mode command")
                elif command == 'connect':
                    self.connect_serial()
                elif command == 'disconnect':
                    self.disconnect_serial()
                elif command == 'status':
                    print(f"\n📊 Mode: {self.mode_names[self.mode]}")
                    print(f"🔌 Serial: {'Connected' if self.serial_connected else 'Disconnected'}")
                    print(f"📹 Camera: {'Active' if self.camera_active else 'Inactive'}")
                    self.show_visual_status()
                elif command == 'visual':
                    self.show_visual_status()
                elif command == 'list' and self.mode == 1:
                    print(f"🎭 Available gestures: {list(self.gestures.keys())}")
                elif command == 'camera start' and self.mode == 2:
                    self.start_camera_tracking()
                elif command == 'camera stop' and self.mode == 2:
                    self.stop_camera_tracking()
                elif command.startswith('set ') and self.mode == 0:
                    self.send_command_to_esp32(command.upper())
                elif command.startswith('get ') and self.mode == 0:
                    self.send_command_to_esp32(command.upper())
                elif command.startswith('gesture ') and self.mode == 1:
                    self.send_command_to_esp32(command.upper())
                elif command.startswith('mimic ') and self.mode == 2:
                    self.send_command_to_esp32(command.upper())
                elif command == '':
                    continue
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Cleanup
        self.stop_camera_tracking()
        self.disconnect_serial()
        print("✅ Simulator stopped")

def run_demo_mode():
    """Run automated demo without user input"""
    print("🎬 === Running Demo Mode ===")
    
    simulator = RoboticHandSimulator()
    
    # Demo sequence
    demo_commands = [
        ("Gesture Demo", [
            "GESTURE open",
            "GESTURE fist", 
            "GESTURE peace",
            "GESTURE thumbs_up",
            "GESTURE point"
        ]),
        ("Individual Finger Demo", [
            "SET 0 0",   # Thumb closed
            "SET 1 180", # Index open
            "SET 2 90",  # Middle half
            "SET 3 45",  # Ring quarter
            "SET 4 135"  # Pinky 3/4
        ]),
        ("Random Movement Demo", [])
    ]
    
    for demo_name, commands in demo_commands:
        print(f"\n🎯 {demo_name}")
        time.sleep(2)
        
        if demo_name == "Random Movement Demo":
            # Generate random movements
            for _ in range(10):
                finger = random.randint(0, 4)
                angle = random.randint(0, 180)
                command = f"SET {finger} {angle}"
                print(f"🎲 Random: {command}")
                simulator.process_command_locally(command)
                simulator.show_visual_status()
                time.sleep(1)
        else:
            for command in commands:
                print(f"🤖 Executing: {command}")
                simulator.process_command_locally(command)
                simulator.show_visual_status()
                time.sleep(2)
    
    print("\n🎬 Demo completed!")

def test_servo_mapping():
    """Test servo angle to PWM mapping"""
    print("🔧 === Testing Servo Mapping ===")
    
    # Simulate ESP32 servo mapping
    MIN_DUTY = 26   # ~0.5ms pulse width (0 degrees)
    MAX_DUTY = 128  # ~2.5ms pulse width (180 degrees)
    
    def angle_to_duty(angle):
        angle = max(0, min(180, angle))
        duty = MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)
        return int(duty)
    
    test_angles = [0, 30, 45, 90, 135, 150, 180]
    
    print("Angle -> Duty Cycle Mapping:")
    for angle in test_angles:
        duty = angle_to_duty(angle)
        pulse_width = (duty / 1023) * 20  # Convert to milliseconds
        print(f"  {angle:>3}° -> Duty: {duty:>3} -> Pulse: {pulse_width:.2f}ms")

def main():
    """Main entry point"""
    print("🤖 === Robotic Hand Control System ===")
    print("Choose mode:")
    print("1. Interactive Simulator")
    print("2. Demo Mode")
    print("3. Test Servo Mapping")
    print("4. Quick Test")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            simulator = RoboticHandSimulator()
            simulator.run_interactive()
        elif choice == "2":
            run_demo_mode()
        elif choice == "3":
            test_servo_mapping()
        elif choice == "4":
            # Quick test mode
            print("🚀 Quick Test Mode")
            simulator = RoboticHandSimulator()
            
            # Test basic commands
            test_commands = [
                "SET 0 90",
                "SET 1 45", 
                "GESTURE fist",
                "GESTURE open",
                "MIMIC 90,45,135,60,120"
            ]
            
            for cmd in test_commands:
                print(f"\n🧪 Testing: {cmd}")
                simulator.process_command_locally(cmd)
                simulator.show_visual_status()
                time.sleep(1)
        else:
            print("Invalid option selected")
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
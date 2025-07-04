"""
Real-time Hand Tracking for ESP32-CAM Robotic Hand Controller
Uses MediaPipe Hands to track finger positions and calculate bend angles.
Sends servo control commands via serial to ESP32-CAM controller.

Requirements:
pip install opencv-python mediapipe pyserial numpy

Hardware Setup:
- ESP32-CAM with 5 servo motors connected
- USB connection to computer for serial communication
- Webcam for hand tracking

Author: AI Assistant
"""

import cv2
import mediapipe as mp
import numpy as np
import serial
import time
import math
from collections import deque
import sys

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Change to 'COM3' on Windows
SERIAL_BAUDRATE = 115200
SEND_INTERVAL = 0.15  # Send data every 150ms
SMOOTHING_WINDOW = 5  # Moving average window size

# MediaPipe configuration
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Finger landmark indices for MediaPipe Hands
FINGER_LANDMARKS = {
    'thumb': [1, 2, 3, 4],      # CMC, MCP, IP, TIP
    'index': [5, 6, 7, 8],      # MCP, PIP, DIP, TIP
    'middle': [9, 10, 11, 12],  # MCP, PIP, DIP, TIP
    'ring': [13, 14, 15, 16],   # MCP, PIP, DIP, TIP
    'pinky': [17, 18, 19, 20]   # MCP, PIP, DIP, TIP
}

class AngleFilter:
    """Smooths angle values using moving average"""
    
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)
    
    def update(self, value):
        """Add new value and return smoothed result"""
        self.values.append(value)
        return sum(self.values) / len(self.values)
    
    def reset(self):
        """Clear the filter"""
        self.values.clear()

class HandTracker:
    """Real-time hand tracking and finger angle calculation"""
    
    def __init__(self, serial_port=SERIAL_PORT, baudrate=SERIAL_BAUDRATE):
        # Initialize MediaPipe Hands
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Initialize serial connection
        self.serial_connection = None
        self.init_serial(serial_port, baudrate)
        
        # Initialize angle filters for each finger
        self.angle_filters = {
            'thumb': AngleFilter(SMOOTHING_WINDOW),
            'index': AngleFilter(SMOOTHING_WINDOW),
            'middle': AngleFilter(SMOOTHING_WINDOW),
            'ring': AngleFilter(SMOOTHING_WINDOW),
            'pinky': AngleFilter(SMOOTHING_WINDOW)
        }
        
        # Store previous angles for fallback
        self.previous_angles = [90, 90, 90, 90, 90]  # Default middle position
        self.last_send_time = time.time()
        
        # Calibration parameters (adjust these for better accuracy)
        self.calibration = {
            'thumb': {'min_angle': 20, 'max_angle': 160},
            'index': {'min_angle': 10, 'max_angle': 170},
            'middle': {'min_angle': 10, 'max_angle': 170},
            'ring': {'min_angle': 15, 'max_angle': 165},
            'pinky': {'min_angle': 20, 'max_angle': 160}
        }
        
        print("Hand Tracker initialized!")
        print(f"Serial port: {serial_port}")
        print("Press 'q' to quit, 'r' to reset filters")
    
    def init_serial(self, port, baudrate):
        """Initialize serial connection to ESP32-CAM"""
        try:
            self.serial_connection = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for connection to establish
            print(f"Serial connection established on {port}")
        except Exception as e:
            print(f"Warning: Could not establish serial connection: {e}")
            print("Running in display-only mode")
    
    def calculate_angle(self, p1, p2, p3):
        """
        Calculate angle between three points (p1-p2-p3)
        Returns angle in degrees (0-180)
        """
        # Convert to numpy arrays
        p1, p2, p3 = np.array(p1), np.array(p2), np.array(p3)
        
        # Calculate vectors
        v1 = p1 - p2
        v2 = p3 - p2
        
        # Calculate angle using dot product
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_angle = np.clip(cos_angle, -1, 1)  # Ensure valid range
        angle = math.degrees(math.acos(cos_angle))
        
        return angle
    
    def get_finger_angle(self, landmarks, finger_name):
        """
        Calculate bend angle for a specific finger
        Returns angle in 0-180 range (0=curled, 180=straight)
        """
        finger_points = FINGER_LANDMARKS[finger_name]
        
        if finger_name == 'thumb':
            # For thumb, use different calculation due to its unique movement
            # Use CMC-MCP-IP points
            p1 = [landmarks[finger_points[0]].x, landmarks[finger_points[0]].y]
            p2 = [landmarks[finger_points[1]].x, landmarks[finger_points[1]].y]
            p3 = [landmarks[finger_points[2]].x, landmarks[finger_points[2]].y]
        else:
            # For other fingers, use MCP-PIP-DIP points
            p1 = [landmarks[finger_points[0]].x, landmarks[finger_points[0]].y]
            p2 = [landmarks[finger_points[1]].x, landmarks[finger_points[1]].y]
            p3 = [landmarks[finger_points[2]].x, landmarks[finger_points[2]].y]
        
        # Calculate raw angle
        raw_angle = self.calculate_angle(p1, p2, p3)
        
        # Apply calibration mapping
        cal = self.calibration[finger_name]
        
        # Map raw angle to 0-180 range
        # Smaller joint angles typically mean more curled fingers
        if raw_angle < cal['min_angle']:
            mapped_angle = 0
        elif raw_angle > cal['max_angle']:
            mapped_angle = 180
        else:
            # Linear mapping
            mapped_angle = ((raw_angle - cal['min_angle']) / 
                          (cal['max_angle'] - cal['min_angle'])) * 180
        
        return int(mapped_angle)
    
    def process_hand_landmarks(self, landmarks):
        """Process hand landmarks and return finger angles"""
        finger_angles = []
        finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
        
        for finger_name in finger_names:
            # Calculate raw angle
            raw_angle = self.get_finger_angle(landmarks, finger_name)
            
            # Apply smoothing filter
            smoothed_angle = self.angle_filters[finger_name].update(raw_angle)
            
            # Clamp to valid range
            smoothed_angle = max(0, min(180, int(smoothed_angle)))
            finger_angles.append(smoothed_angle)
        
        return finger_angles
    
    def send_to_robot(self, angles):
        """Send angle data to ESP32-CAM via serial"""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Format command for ESP32-CAM
                command = f"MIMIC {','.join(map(str, angles))}\n"
                self.serial_connection.write(command.encode())
                print(f"Sent: {command.strip()}")
            except Exception as e:
                print(f"Serial send error: {e}")
        else:
            print(f"No serial connection - would send: {angles}")
    
    def draw_finger_info(self, image, angles, landmarks=None):
        """Draw finger angle information on the image"""
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        
        # Draw angle information
        y_offset = 30
        for i, (name, angle) in enumerate(zip(finger_names, angles)):
            color = (0, 255, 0) if angle > 90 else (0, 255, 255)  # Green if extended, yellow if curled
            cv2.putText(image, f"{name}: {angle}°", (10, y_offset + i * 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Draw connection status
        status_color = (0, 255, 0) if (self.serial_connection and 
                                     self.serial_connection.is_open) else (0, 0, 255)
        status_text = "Serial: Connected" if (self.serial_connection and 
                                            self.serial_connection.is_open) else "Serial: Disconnected"
        cv2.putText(image, status_text, (10, image.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Draw hand landmarks if available
        if landmarks:
            mp_drawing.draw_landmarks(
                image, landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    
    def run(self):
        """Main tracking loop"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        # Set camera resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Starting hand tracking...")
        print("Controls:")
        print("  'q' - Quit")
        print("  'r' - Reset angle filters")
        print("  'c' - Toggle calibration display")
        
        show_calibration = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = self.hands.process(rgb_frame)
            
            current_angles = self.previous_angles.copy()  # Fallback to previous
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Calculate finger angles
                    current_angles = self.process_hand_landmarks(hand_landmarks.landmark)
                    
                    # Update previous angles
                    self.previous_angles = current_angles
                    
                    # Draw landmarks and info
                    self.draw_finger_info(frame, current_angles, hand_landmarks)
                    
                    break  # Only process first hand
            else:
                # No hand detected - use previous angles
                self.draw_finger_info(frame, current_angles)
                cv2.putText(frame, "No hand detected", (10, 160),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Send data at regular intervals
            current_time = time.time()
            if current_time - self.last_send_time >= SEND_INTERVAL:
                self.send_to_robot(current_angles)
                self.last_send_time = current_time
            
            # Show calibration info if requested
            if show_calibration:
                y_pos = 200
                cv2.putText(frame, "Calibration Ranges:", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                for i, (finger, cal) in enumerate(self.calibration.items()):
                    text = f"{finger}: {cal['min_angle']}-{cal['max_angle']}"
                    cv2.putText(frame, text, (10, y_pos + 20 + i * 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Display frame
            cv2.imshow('Hand Tracking - Robotic Hand Controller', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('r'):
                print("Resetting angle filters...")
                for filter_obj in self.angle_filters.values():
                    filter_obj.reset()
            elif key == ord('c'):
                show_calibration = not show_calibration
                print(f"Calibration display: {'ON' if show_calibration else 'OFF'}")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        if self.serial_connection and self.serial_connection.is_open:
            # Send neutral position before closing
            self.send_to_robot([90, 90, 90, 90, 90])
            time.sleep(0.5)
            self.serial_connection.close()
            print("Serial connection closed")

def main():
    """Main function"""
    print("ESP32-CAM Robotic Hand Controller")
    print("=================================")
    
    # Configuration
    serial_port = SERIAL_PORT
    if len(sys.argv) > 1:
        serial_port = sys.argv[1]
        print(f"Using serial port from command line: {serial_port}")
    
    try:
        tracker = HandTracker(serial_port=serial_port)
        tracker.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Hand tracking stopped")

if __name__ == "__main__":
    main()
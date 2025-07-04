"""
Real-time Hand Tracking for Robotic Hand Control
PC-side application that tracks human hand movements and sends finger bend angles
to an ESP32-CAM robotic hand via serial communication.

Features:
- Real-time hand tracking using MediaPipe
- Finger bend angle calculation (0-180°)
- Serial communication with ESP32-CAM
- Smoothing filters for stable control
- Visual feedback and debugging overlay
- Auto-detection of serial ports
- Configurable parameters

Requirements:
- opencv-python
- mediapipe
- numpy
- pyserial

Author: AI Assistant
Date: 2025
"""

import cv2
import mediapipe as mp
import numpy as np
import serial
import serial.tools.list_ports
import time
import threading
import queue
from typing import List, Tuple, Optional, Dict
import sys
import math

class AngleFilter:
    """Exponential smoothing filter for angle values"""
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize filter with smoothing factor
        Args:
            alpha: Smoothing factor (0-1), lower = more smoothing
        """
        self.alpha = alpha
        self.filtered_values = None
        self.initialized = False
    
    def update(self, new_values: List[float]) -> List[float]:
        """
        Update filter with new angle values
        Args:
            new_values: List of 5 finger angles
        Returns:
            Filtered angle values
        """
        if not self.initialized:
            self.filtered_values = new_values.copy()
            self.initialized = True
            return self.filtered_values
        
        # Apply exponential smoothing
        for i in range(len(new_values)):
            self.filtered_values[i] = (self.alpha * new_values[i] + 
                                     (1 - self.alpha) * self.filtered_values[i])
        
        return self.filtered_values.copy()
    
    def reset(self):
        """Reset filter state"""
        self.initialized = False
        self.filtered_values = None

class SerialCommunicator:
    """Handles serial communication with ESP32-CAM"""
    
    def __init__(self, port: str = None, baudrate: int = 115200):
        """
        Initialize serial communicator
        Args:
            port: Serial port name (e.g., 'COM3' or '/dev/ttyUSB0')
            baudrate: Communication speed
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.connected = False
        self.command_queue = queue.Queue()
        self.last_send_time = 0
        self.send_interval = 0.15  # 150ms between commands
        
    def list_available_ports(self) -> List[str]:
        """
        List all available serial ports
        Returns:
            List of available port names
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def connect(self, port: str = None) -> bool:
        """
        Connect to serial port
        Args:
            port: Optional port name override
        Returns:
            True if connection successful
        """
        if port:
            self.port = port
        
        if not self.port:
            print("❌ No serial port specified")
            return False
        
        try:
            self.serial_connection = serial.Serial(
                self.port, 
                self.baudrate, 
                timeout=1
            )
            self.connected = True
            print(f"✅ Connected to {self.port} at {self.baudrate} baud")
            
            # Start communication thread
            self.comm_thread = threading.Thread(
                target=self._communication_loop, 
                daemon=True
            )
            self.comm_thread.start()
            
            return True
            
        except serial.SerialException as e:
            print(f"❌ Failed to connect to {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from serial port"""
        if self.serial_connection and self.connected:
            self.connected = False
            self.serial_connection.close()
            print(f"🔌 Disconnected from {self.port}")
    
    def send_angles(self, angles: List[int]) -> bool:
        """
        Send finger angles to ESP32-CAM
        Args:
            angles: List of 5 finger angles (0-180°)
        Returns:
            True if command was queued successfully
        """
        current_time = time.time()
        
        # Rate limiting
        if current_time - self.last_send_time < self.send_interval:
            return False
        
        self.last_send_time = current_time
        
        # Format command
        angle_str = ','.join(map(str, angles))
        command = f"MIMIC {angle_str}"
        
        if self.connected:
            try:
                self.command_queue.put(command, block=False)
                return True
            except queue.Full:
                print("⚠️ Command queue full")
                return False
        else:
            # Print command for debugging when not connected
            print(f"🤖 Would send: {command}")
            return True
    
    def _communication_loop(self):
        """Background thread for serial communication"""
        while self.connected and self.serial_connection:
            try:
                # Send queued commands
                try:
                    command = self.command_queue.get_nowait()
                    self.serial_connection.write(f"{command}\n".encode())
                    print(f"📤 Sent: {command}")
                except queue.Empty:
                    pass
                
                # Read responses (optional)
                if self.serial_connection.in_waiting > 0:
                    response = self.serial_connection.readline().decode().strip()
                    if response:
                        print(f"📥 ESP32: {response}")
                
                time.sleep(0.01)
                
            except Exception as e:
                print(f"❌ Communication error: {e}")
                break

class HandTracker:
    """MediaPipe-based hand tracking and angle calculation"""
    
    def __init__(self, min_detection_confidence: float = 0.7, 
                 min_tracking_confidence: float = 0.5):
        """
        Initialize hand tracker
        Args:
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Finger landmark indices for angle calculation
        self.finger_landmarks = {
            'thumb': [2, 3, 4],      # CMC, MCP, IP joints
            'index': [5, 6, 8],      # MCP, PIP, TIP
            'middle': [9, 10, 12],   # MCP, PIP, TIP
            'ring': [13, 14, 16],    # MCP, PIP, TIP
            'pinky': [17, 18, 20]    # MCP, PIP, TIP
        }
        
        self.finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
        
    def calculate_angle(self, p1: Tuple[float, float], 
                       p2: Tuple[float, float], 
                       p3: Tuple[float, float]) -> float:
        """
        Calculate angle between three points using cosine law
        Args:
            p1, p2, p3: Points as (x, y) tuples
            p2 is the vertex of the angle
        Returns:
            Angle in degrees
        """
        # Create vectors
        v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        
        # Calculate angle using dot product
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        
        # Clamp to valid range to avoid numerical errors
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        # Calculate angle in degrees
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def get_finger_angles(self, landmarks) -> List[float]:
        """
        Calculate bend angles for all fingers
        Args:
            landmarks: MediaPipe hand landmarks
        Returns:
            List of 5 finger bend angles (0-180°)
        """
        angles = []
        
        for finger_name in self.finger_names:
            landmark_indices = self.finger_landmarks[finger_name]
            
            # Get 3D coordinates for the three points
            p1 = landmarks.landmark[landmark_indices[0]]
            p2 = landmarks.landmark[landmark_indices[1]]
            p3 = landmarks.landmark[landmark_indices[2]]
            
            # Convert to 2D coordinates (using x, y)
            point1 = (p1.x, p1.y)
            point2 = (p2.x, p2.y)
            point3 = (p3.x, p3.y)
            
            # Calculate angle
            angle = self.calculate_angle(point1, point2, point3)
            
            # Normalize angle to 0-180° range
            # Straight finger should be ~180°, bent finger ~0°
            normalized_angle = 180 - angle
            normalized_angle = max(0, min(180, normalized_angle))
            
            angles.append(normalized_angle)
        
        return angles
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[List[float]]]:
        """
        Process video frame and extract hand angles
        Args:
            frame: Input video frame
        Returns:
            Tuple of (annotated_frame, finger_angles)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        annotated_frame = frame.copy()
        finger_angles = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Calculate finger angles
                finger_angles = self.get_finger_angles(hand_landmarks)
                
                # Only process first detected hand
                break
        
        return annotated_frame, finger_angles

class HandControlApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the hand control application"""
        self.hand_tracker = HandTracker()
        self.angle_filter = AngleFilter(alpha=0.3)
        self.serial_comm = SerialCommunicator()
        
        self.cap = None
        self.running = False
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        self.last_angles = [90, 90, 90, 90, 90]  # Default middle position
        
    def setup_camera(self, camera_id: int = 0) -> bool:
        """
        Initialize camera capture
        Args:
            camera_id: Camera device ID
        Returns:
            True if camera initialized successfully
        """
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            print(f"❌ Cannot open camera {camera_id}")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"✅ Camera {camera_id} initialized")
        return True
    
    def setup_serial(self) -> bool:
        """
        Setup serial communication
        Returns:
            True if serial setup successful
        """
        # List available ports
        available_ports = self.serial_comm.list_available_ports()
        
        if not available_ports:
            print("⚠️ No serial ports found. Running in simulation mode.")
            return False
        
        print("🔍 Available serial ports:")
        for i, port in enumerate(available_ports):
            print(f"  {i + 1}: {port}")
        
        # Let user choose port
        try:
            print("\nEnter port number (or 0 to run without serial connection):")
            choice = input("Choice: ").strip()
            
            if choice == "0":
                print("⚠️ Running without serial connection")
                return False
            
            port_index = int(choice) - 1
            if 0 <= port_index < len(available_ports):
                selected_port = available_ports[port_index]
                return self.serial_comm.connect(selected_port)
            else:
                print("❌ Invalid port selection")
                return False
                
        except (ValueError, KeyboardInterrupt):
            print("⚠️ Running without serial connection")
            return False
    
    def draw_overlay(self, frame: np.ndarray, angles: List[float]) -> np.ndarray:
        """
        Draw debugging overlay on frame
        Args:
            frame: Input frame
            angles: Current finger angles
        Returns:
            Frame with overlay
        """
        height, width = frame.shape[:2]
        
        # Draw semi-transparent background for text
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 200), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Draw finger angles
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        for i, (name, angle) in enumerate(zip(finger_names, angles)):
            y_pos = 35 + i * 25
            
            # Color based on angle (red = bent, green = straight)
            color_intensity = int(angle / 180 * 255)
            color = (0, color_intensity, 255 - color_intensity)
            
            text = f"{name}: {angle:3.0f}°"
            cv2.putText(frame, text, (20, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Draw FPS
        fps_text = f"FPS: {self.current_fps:.1f}"
        cv2.putText(frame, fps_text, (20, height - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw connection status
        status_text = "Connected" if self.serial_comm.connected else "Disconnected"
        status_color = (0, 255, 0) if self.serial_comm.connected else (0, 0, 255)
        cv2.putText(frame, f"Serial: {status_text}", (20, height - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Draw instructions
        instructions = [
            "Press 'q' to quit",
            "Press 'r' to reset filter",
            "Press 'c' to recalibrate"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = height - 120 + i * 20
            cv2.putText(frame, instruction, (width - 250, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def update_fps(self):
        """Update FPS counter"""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def run(self):
        """Main application loop"""
        print("🤖 === Hand Control Application ===")
        
        # Setup camera
        if not self.setup_camera():
            return
        
        # Setup serial (optional)
        self.setup_serial()
        
        print("\n🚀 Starting hand tracking...")
        print("Press 'q' to quit, 'r' to reset filter, 'c' to recalibrate")
        
        self.running = True
        
        try:
            while self.running:
                # Capture frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to capture frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame
                annotated_frame, raw_angles = self.hand_tracker.process_frame(frame)
                
                if raw_angles is not None:
                    # Filter angles
                    filtered_angles = self.angle_filter.update(raw_angles)
                    
                    # Convert to integers
                    int_angles = [int(angle) for angle in filtered_angles]
                    
                    # Send to ESP32
                    self.serial_comm.send_angles(int_angles)
                    
                    # Update last known angles
                    self.last_angles = int_angles
                    
                    # Draw overlay
                    display_frame = self.draw_overlay(annotated_frame, int_angles)
                else:
                    # No hand detected, show last known angles
                    display_frame = self.draw_overlay(annotated_frame, self.last_angles)
                
                # Update FPS
                self.update_fps()
                
                # Display frame
                cv2.imshow('Hand Control', display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.angle_filter.reset()
                    print("🔄 Filter reset")
                elif key == ord('c'):
                    # Recalibration placeholder
                    print("🎯 Recalibration (not implemented)")
                
        except KeyboardInterrupt:
            print("\n⏹️ Interrupted by user")
        
        finally:
            # Cleanup
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        self.serial_comm.disconnect()
        
        print("✅ Cleanup complete")

def main():
    """Main entry point"""
    try:
        app = HandControlApp()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
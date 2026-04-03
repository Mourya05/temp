"""
Main Student Attendance System using Facial Recognition
Optimized for Raspberry Pi 4/5 with threading and performance optimizations
"""

import cv2
import threading
import time
import sys
import pickle
from datetime import datetime
from queue import Queue
import numpy as np

from database_handler import AttendanceDatabase
from face_recognition import FaceRecognitionEngine


class AttendanceSystem:
    """Main attendance system with camera polling and face recognition"""
    
    def __init__(self, headless_mode=False, camera_id=0, frame_width=640, frame_height=480, scale_factor=0.5):
        """
        Initialize the attendance system
        
        Args:
            headless_mode: If True, use console output only. If False, use GUI.
            camera_id: Camera device ID (default 0)
            frame_width: Desired frame width
            frame_height: Desired frame height
            scale_factor: Scale factor for frame resizing (0.5 = 50% of original)
        """
        print("[SYSTEM] Initializing Student Attendance System...")
        
        self.headless_mode = headless_mode
        self.camera_id = camera_id
        self.frame_width = int(frame_width * scale_factor)
        self.frame_height = int(frame_height * scale_factor)
        self.scale_factor = scale_factor
        
        # Threading components
        self.is_running = False
        self.frame_queue = Queue(maxsize=2)  # Small queue to prevent lag
        self.camera_thread = None
        self.processing_thread = None
        
        # Initialize components
        self.db = AttendanceDatabase()
        self.face_engine = FaceRecognitionEngine(model_confidence=0.5)
        
        # Load known faces from database
        students = self.db.get_all_students()
        self.face_engine.load_known_faces_from_db(students)
        
        # Debounce tracking: {student_id: last_detection_time}
        self.last_detection_time = {}
        self.debounce_seconds = 60
        
        # FPS tracking
        self.fps = 0
        self.frame_count = 0
        self.fps_start_time = time.time()
        
        print("[SYSTEM] Initialization complete")
    
    def camera_polling_thread(self):
        """
        Thread function for continuous camera polling
        Captures frames and puts them in queue with minimal processing
        """
        print("[CAMERA] Starting camera polling thread...")
        
        try:
            cap = cv2.VideoCapture(self.camera_id)
            
            if not cap.isOpened():
                print("[ERROR] Could not open camera")
                return
            
            # Set camera resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer
            
            print(f"[CAMERA] Camera opened: {self.frame_width}x{self.frame_height}")
            
            while self.is_running:
                ret, frame = cap.read()
                
                if ret:
                    # Resize frame if needed
                    frame = cv2.resize(frame, (self.frame_width, self.frame_height))
                    
                    # Drop oldest frame if queue is full
                    try:
                        self.frame_queue.get_nowait()
                    except:
                        pass
                    
                    self.frame_queue.put(frame)
                else:
                    print("[WARNING] Failed to capture frame")
                    time.sleep(0.01)
            
            cap.release()
            print("[CAMERA] Camera polling thread stopped")
        
        except Exception as e:
            print(f"[ERROR] Camera thread error: {e}")
    
    def processing_thread_func(self):
        """
        Thread function for face detection and recognition
        Processes frames from queue
        """
        print("[PROCESSOR] Starting face processing thread...")
        
        while self.is_running:
            try:
                frame = self.frame_queue.get(timeout=1)
                
                # Detect faces
                faces = self.face_engine.detect_faces(frame)
                
                if len(faces) > 0:
                    labels = []
                    for face_data in faces:
                        embedding = face_data['embedding']
                        
                        # Recognize face
                        student_id, name, confidence = self.face_engine.recognize_face(embedding)
                        
                        if student_id is not None:
                            # Check debounce logic
                            current_time = time.time()
                            last_time = self.last_detection_time.get(student_id, 0)
                            
                            if current_time - last_time > self.debounce_seconds:
                                # Mark attendance
                                success = self.db.mark_attendance(student_id, "Present")
                                if success:
                                    self.last_detection_time[student_id] = current_time
                                    message = f"✓ ACCESS GRANTED: {name}"
                                    print(f"\n[ATTENDANCE] {message}")
                                    if not self.headless_mode:
                                        self.show_notification(message, is_approved=True)
                                    labels.append(name)
                                else:
                                    labels.append(f"{name} (DB Error)")
                            else:
                                # Too soon, skip
                                labels.append(f"{name} (Recent)")
                        else:
                            # Unknown face
                            labels.append("Unknown")
                            self.db.log_unknown_face()
                            if not self.headless_mode:
                                self.show_notification("Unknown face detected", is_approved=False)
                    
                    # Draw on frame
                    if not self.headless_mode:
                        frame = self.face_engine.draw_face_boxes(frame, faces, labels)
                
                # Update FPS
                self.frame_count += 1
                elapsed = time.time() - self.fps_start_time
                if elapsed > 1:
                    self.fps = self.frame_count / elapsed
                    self.frame_count = 0
                    self.fps_start_time = time.time()
                
                # Display frame if GUI mode
                if not self.headless_mode:
                    self.display_frame(frame)
            
            except Exception as e:
                if self.is_running:
                    print(f"[ERROR] Processing thread error: {e}")
    
    def display_frame(self, frame):
        """Display frame in GUI mode with FPS counter"""
        if frame is not None:
            # Add FPS counter
            text = f"FPS: {self.fps:.1f}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Student Attendance System', frame)
            
            # Handle key press 'q' to quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.stop()
    
    def show_notification(self, message, is_approved=True):
        """Display notification (can be extended for GUI)"""
        if is_approved:
            print(f"[NOTIFICATION] {message}")
        else:
            print(f"[SECURITY] {message}")
    
    def start(self):
        """Start the attendance system"""
        print("[SYSTEM] Starting attendance system...")
        self.is_running = True
        
        # Start camera polling thread
        self.camera_thread = threading.Thread(target=self.camera_polling_thread, daemon=True)
        self.camera_thread.start()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.processing_thread_func, daemon=True)
        self.processing_thread.start()
        
        print("[SYSTEM] System running. Press Ctrl+C to stop (or 'q' in GUI mode)...")
        
        # Keep main thread alive
        try:
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[SYSTEM] Keyboard interrupt received")
            self.stop()
    
    def stop(self):
        """Stop the attendance system"""
        print("[SYSTEM] Stopping attendance system...")
        self.is_running = False
        
        if self.camera_thread:
            self.camera_thread.join(timeout=2)
        if self.processing_thread:
            self.processing_thread.join(timeout=2)
        
        self.face_engine.cleanup()
        cv2.destroyAllWindows()
        
        print("[SYSTEM] System stopped")
    
    def register_student_from_image(self, name, roll_number, image_path):
        """Register a new student from an image file"""
        print(f"[REGISTRATION] Registering {name} ({roll_number}) from {image_path}")
        
        embedding = self.face_engine.generate_embedding_from_image(image_path)
        
        if embedding is None:
            print("[ERROR] Failed to generate embedding")
            return False
        
        # Serialize embedding
        embedding_blob = pickle.dumps(embedding)
        
        success = self.db.register_student(name, roll_number, embedding_blob)
        
        if success:
            # Reload known faces
            students = self.db.get_all_students()
            self.face_engine.load_known_faces_from_db(students)
        
        return success
    
    def export_attendance(self, output_file="attendance_report.csv"):
        """Export attendance to CSV"""
        return self.db.export_to_csv(output_file)
    
    def get_today_attendance_report(self):
        """Get today's attendance report"""
        records = self.db.get_today_attendance()
        
        print("\n" + "="*60)
        print("TODAY'S ATTENDANCE REPORT")
        print("="*60)
        print(f"{'Student Name':<20} {'Roll Number':<15} {'Count':<10}")
        print("-"*60)
        
        for name, roll_number, count in records:
            print(f"{name:<20} {roll_number:<15} {count:<10}")
        
        print("="*60 + "\n")
        
        return records


class ConsoleInterface:
    """Command-line interface for system management"""
    
    def __init__(self, system):
        self.system = system
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("STUDENT ATTENDANCE SYSTEM - MANAGEMENT MENU")
        print("="*60)
        print("1. Start Attendance Monitoring")
        print("2. Register New Student")
        print("3. View Today's Attendance")
        print("4. Export Attendance to CSV")
        print("5. Delete Student Record")
        print("6. Exit")
        print("="*60)
    
    def run(self):
        """Run the console interface"""
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self.system.start()
            
            elif choice == "2":
                self.register_student()
            
            elif choice == "3":
                self.system.get_today_attendance_report()
            
            elif choice == "4":
                filename = input("Enter output filename (default: attendance_report.csv): ").strip()
                if not filename:
                    filename = "attendance_report.csv"
                self.system.export_attendance(filename)
            
            elif choice == "5":
                self.delete_student()
            
            elif choice == "6":
                print("[SYSTEM] Exiting...")
                break
            
            else:
                print("[ERROR] Invalid choice. Please try again.")
    
    def register_student(self):
        """Register a new student through console"""
        print("\n--- Student Registration ---")
        name = input("Enter student name: ").strip()
        roll_number = input("Enter roll number: ").strip()
        image_path = input("Enter path to student image: ").strip()
        
        if not name or not roll_number or not image_path:
            print("[ERROR] All fields are required")
            return
        
        self.system.register_student_from_image(name, roll_number, image_path)
    
    def delete_student(self):
        """Delete a student record"""
        print("\n--- Delete Student ---")
        roll_number = input("Enter roll number to delete: ").strip()
        
        if self.system.db.delete_student(roll_number):
            # Reload known faces
            students = self.system.db.get_all_students()
            self.system.face_engine.load_known_faces_from_db(students)
        else:
            print("[ERROR] Failed to delete student")


def main():
    """Main entry point"""
    # Check for command-line arguments
    headless_mode = "--headless" in sys.argv
    
    # Initialize system
    system = AttendanceSystem(headless_mode=headless_mode)
    
    if headless_mode:
        # Console mode
        interface = ConsoleInterface(system)
        interface.run()
    else:
        # Quick GUI mode
        print("[SYSTEM] Starting in GUI mode...")
        system.start()


if __name__ == "__main__":
    main()

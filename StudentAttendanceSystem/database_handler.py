"""
Database Handler for Student Attendance System
Using SQLite for local storage and CSV export functionality
"""

import sqlite3
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path


class AttendanceDatabase:
    """Handles all database operations for attendance tracking"""
    
    def __init__(self, db_path="attendance.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create attendance table if it doesn't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_number TEXT UNIQUE NOT NULL,
                    face_encoding BLOB NOT NULL,
                    registered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create attendance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'Present',
                    FOREIGN KEY(student_id) REFERENCES students(student_id)
                )
            """)
            
            # Create unknown faces table for logging unrecognized faces
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unknown_faces (
                    unknown_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    face_image BLOB
                )
            """)
            
            conn.commit()
            conn.close()
            print(f"[DATABASE] Initialized database: {self.db_path}")
        except Exception as e:
            print(f"[ERROR] Failed to initialize database: {e}")
    
    def register_student(self, name, roll_number, face_encoding):
        """Register a new student with face encoding"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO students (name, roll_number, face_encoding)
                VALUES (?, ?, ?)
            """, (name, roll_number, face_encoding))
            
            conn.commit()
            conn.close()
            print(f"[DATABASE] Student registered: {name} ({roll_number})")
            return True
        except sqlite3.IntegrityError:
            print(f"[ERROR] Student {roll_number} already exists")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to register student: {e}")
            return False
    
    def mark_attendance(self, student_id, status="Present"):
        """Mark attendance for a student"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO attendance (student_id, timestamp, status)
                VALUES (?, CURRENT_TIMESTAMP, ?)
            """, (student_id, status))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to mark attendance: {e}")
            return False
    
    def get_student_by_id(self, student_id):
        """Retrieve student information by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cursor.fetchone()
            conn.close()
            
            return student
        except Exception as e:
            print(f"[ERROR] Failed to retrieve student: {e}")
            return None
    
    def get_all_students(self):
        """Retrieve all registered students"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT student_id, name, roll_number, face_encoding FROM students")
            students = cursor.fetchall()
            conn.close()
            
            return students
        except Exception as e:
            print(f"[ERROR] Failed to retrieve students: {e}")
            return []
    
    def check_recent_attendance(self, student_id, minutes=1):
        """Check if student was marked present in the last N minutes (debounce logic)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            time_threshold = datetime.now() - timedelta(minutes=minutes)
            cursor.execute("""
                SELECT COUNT(*) FROM attendance 
                WHERE student_id = ? AND timestamp > ? AND status = 'Present'
            """, (student_id, time_threshold))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
        except Exception as e:
            print(f"[ERROR] Failed to check recent attendance: {e}")
            return False
    
    def log_unknown_face(self, face_image_blob=None):
        """Log unknown face detection for security purposes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO unknown_faces (timestamp, face_image)
                VALUES (CURRENT_TIMESTAMP, ?)
            """, (face_image_blob,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to log unknown face: {e}")
            return False
    
    def export_to_csv(self, output_file="attendance_report.csv"):
        """Export attendance records to CSV file"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.name, s.roll_number, a.timestamp, a.status
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                ORDER BY a.timestamp DESC
            """)
            
            records = cursor.fetchall()
            conn.close()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Student Name', 'Roll Number', 'Timestamp', 'Status'])
                writer.writerows(records)
            
            print(f"[DATABASE] Attendance exported to {output_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to export CSV: {e}")
            return False
    
    def get_today_attendance(self):
        """Get attendance records for today"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            cursor.execute("""
                SELECT s.name, s.roll_number, COUNT(*) as count
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                WHERE DATE(a.timestamp) = ?
                GROUP BY a.student_id
            """, (today,))
            
            records = cursor.fetchall()
            conn.close()
            
            return records
        except Exception as e:
            print(f"[ERROR] Failed to get today's attendance: {e}")
            return []
    
    def delete_student(self, roll_number):
        """Delete a student record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM students WHERE roll_number = ?", (roll_number,))
            conn.commit()
            conn.close()
            
            print(f"[DATABASE] Student {roll_number} deleted")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete student: {e}")
            return False

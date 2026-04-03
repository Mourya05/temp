"""
Configuration and Constants for Attendance System
"""

# Camera settings
CAMERA_ID = 0  # Default camera (0=built-in, 1=USB camera, etc.)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_SCALE_FACTOR = 0.5  # Resize frames to 50% for faster processing

# Face detection settings
FACE_DETECTION_CONFIDENCE = 0.5  # 0.0 to 1.0, higher = stricter
FACE_RECOGNITION_TOLERANCE = 40.0  # Lower = stricter matching
FACE_EMBEDDING_SIZE = 128 * 128  # Size of face embedding

# Attendance settings
DEBOUNCE_SECONDS = 60  # Minimum seconds between same student detections
MAX_UNKNOWN_FACES_LOG = 1000  # Maximum unknown faces to log

# Database settings
DATABASE_PATH = "attendance.db"
DATABASE_TIMEOUT = 10  # SQLite timeout in seconds

# GUI settings (if using Tkinter)
GUI_WIDTH = 1280
GUI_HEIGHT = 720
GUI_TITLE = "Student Attendance System - Facial Recognition"

# Performance settings
THREAD_POLLING_INTERVAL = 0.01  # 10ms between camera polls
PROCESSING_THREAD_TIMEOUT = 1  # 1 second timeout for frame queue
QUEUE_MAX_SIZE = 2  # Maximum frames in processing queue

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "attendance_system.log"

# Paths
DATASET_DIR = "./dataset"
KNOWN_FACES_DIR = "./dataset/known_faces"
UNKNOWN_FACES_DIR = "./dataset/unknown_faces"
REPORTS_DIR = "./reports"
PHOTOS_DIR = "./student_photos"

# File extensions
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']

# Alerts and notifications
ALERT_SOUND_ENABLED = False  # Set to True to play sound on detection
ALERT_SOUND_PATH = "./sounds/alert.mp3"

# System optimization for Raspberry Pi
USE_GPU = False  # Set to True if using Raspberry Pi with GPU
NUM_WORKERS = 2  # Number of processing threads
BATCH_PROCESS_SIZE = 1  # Process this many frames at once

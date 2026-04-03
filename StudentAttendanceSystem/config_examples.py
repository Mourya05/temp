"""
Example Configuration & Best Practices
Student Attendance System
"""

# ============================================================================
# CAMERA CONFIGURATION
# ============================================================================

class CameraConfig:
    """Camera settings for different use cases"""
    
    # Raspberry Pi with USB camera (Standard)
    PI_USB_CAMERA = {
        'camera_id': 0,
        'frame_width': 640,
        'frame_height': 480,
        'scale_factor': 0.5,        # 50% scaling for performance
        'fps_target': 15,
    }
    
    # Raspberry Pi with CSI camera (Ribbon)
    PI_CSI_CAMERA = {
        'camera_id': 0,
        'frame_width': 640,
        'frame_height': 480,
        'scale_factor': 0.5,
        'fps_target': 20,
    }
    
    # Desktop PC with high-end GPU
    PC_HIGH_END = {
        'camera_id': 0,
        'frame_width': 1920,
        'frame_height': 1440,
        'scale_factor': 1.0,        # No scaling
        'fps_target': 30,
    }
    
    # Laptop/Low Power Device
    LAPTOP_LOW_POWER = {
        'camera_id': 0,
        'frame_width': 320,
        'frame_height': 240,
        'scale_factor': 0.25,       # 25% scaling
        'fps_target': 10,
    }
    
    # Outdoor/High Light Environment
    OUTDOOR = {
        'camera_id': 0,
        'frame_width': 480,
        'frame_height': 360,
        'scale_factor': 0.75,
        'fps_target': 20,          # Slightly higher for better detection
    }


# ============================================================================
# DATABASE CONFIGURATIONS
# ============================================================================

class DatabaseConfig:
    """Database settings for different scenarios"""
    
    # Standard SQLite (Single machine)
    STANDARD = {
        'database_path': 'attendance.db',
        'timeout': 10,
        'wal_mode': True,          # Write-Ahead Logging for better concurrency
        'backup_interval': 3600,   # Backup every hour
    }
    
    # High-Volume Setup (Large class)
    HIGH_VOLUME = {
        'database_path': 'attendance.db',
        'timeout': 20,
        'wal_mode': True,
        'batch_size': 50,          # Batch inserts
        'backup_interval': 1800,   # Backup every 30 min
    }
    
    # External Storage (Raspberry Pi + SSD)
    EXTERNAL_SSD = {
        'database_path': '/mnt/ssd/attendance.db',
        'timeout': 10,
        'wal_mode': True,
        'backup_interval': 3600,
    }


# ============================================================================
# FACE RECOGNITION PARAMETERS
# ============================================================================

class FaceRecognitionConfig:
    """Face recognition tuning for different scenarios"""
    
    # Strict Recognition (Minimize false positives)
    STRICT = {
        'detection_confidence': 0.7,
        'recognition_tolerance': 35.0,     # Stricter matching
        'min_face_size': 50,
        'debounce_seconds': 120,           # 2 minutes
    }
    
    # Balanced Recognition (Default)
    BALANCED = {
        'detection_confidence': 0.5,
        'recognition_tolerance': 40.0,
        'min_face_size': 40,
        'debounce_seconds': 60,            # 1 minute
    }
    
    # Lenient Recognition (Maximize true positives)
    LENIENT = {
        'detection_confidence': 0.3,
        'recognition_tolerance': 50.0,     # More forgiving
        'min_face_size': 30,
        'debounce_seconds': 45,
    }
    
    # Security-Focused (Log all unknowns)
    SECURITY = {
        'detection_confidence': 0.8,
        'recognition_tolerance': 30.0,
        'min_face_size': 60,
        'debounce_seconds': 180,           # 3 minutes
        'log_unknown_faces': True,
        'log_unconfident_matches': True,
    }


# ============================================================================
# PERFORMANCE PROFILES
# ============================================================================

class PerformanceProfile:
    """Pre-configured performance profiles"""
    
    # Raspberry Pi 4 - Balanced
    PI4_BALANCED = {
        'frame_scale_factor': 0.5,
        'queue_size': 2,
        'num_workers': 2,
        'detection_confidence': 0.5,
        'debounce_seconds': 60,
        'enable_gpu': False,
    }
    
    # Raspberry Pi 4 - Maximum Performance
    PI4_MAX_PERFORMANCE = {
        'frame_scale_factor': 0.25,        # Faster processing
        'queue_size': 1,                   # Minimize latency
        'num_workers': 1,                  # Single thread for Pi
        'detection_confidence': 0.3,       # More lenient
        'debounce_seconds': 90,            # Avoid spam
        'enable_gpu': False,
    }
    
    # Raspberry Pi 5 - High Quality
    PI5_HIGH_QUALITY = {
        'frame_scale_factor': 0.75,
        'queue_size': 3,
        'num_workers': 3,
        'detection_confidence': 0.6,
        'debounce_seconds': 60,
        'enable_gpu': False,
    }
    
    # Desktop PC - High Quality
    PC_HIGH_QUALITY = {
        'frame_scale_factor': 1.0,         # Full resolution
        'queue_size': 5,
        'num_workers': 4,
        'detection_confidence': 0.7,
        'debounce_seconds': 60,
        'enable_gpu': True,                # GPU acceleration
    }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

"""
from config_examples import *
from attendance_system import AttendanceSystem

# Example 1: Raspberry Pi Setup
pi_config = CameraConfig.PI_USB_CAMERA
perf_config = PerformanceProfile.PI4_BALANCED
face_config = FaceRecognitionConfig.BALANCED

system = AttendanceSystem(
    camera_id=pi_config['camera_id'],
    frame_width=int(pi_config['frame_width'] * pi_config['scale_factor']),
    frame_height=int(pi_config['frame_height'] * pi_config['scale_factor']),
    scale_factor=pi_config['scale_factor']
)

# Example 2: Security-Focused Setup
security_config = FaceRecognitionConfig.SECURITY
system = AttendanceSystem()
# Additional configuration as needed

# Example 3: High-Performance Desktop
desktop_config = CameraConfig.PC_HIGH_END
system = AttendanceSystem(
    camera_id=desktop_config['camera_id'],
    frame_width=desktop_config['frame_width'],
    frame_height=desktop_config['frame_height'],
    scale_factor=desktop_config['scale_factor']
)
"""


# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
BEST PRACTICES FOR STUDENT ATTENDANCE SYSTEM

1. DATASET MANAGEMENT
   ✓ Use 3-5 photos per student (front, left, right angles)
   ✓ Ensure good lighting in all photos
   ✓ Face should be 30-70% of image
   ✓ Use consistent naming: StudentName_RollNumber
   ✓ Regularly validate dataset quality
   ✓ Retrain monthly for accuracy

2. PERFORMANCE OPTIMIZATION
   ✓ Use Raspberry Pi Lite OS (no desktop)
   ✓ Enable WAL mode in SQLite for faster I/O
   ✓ Use external SSD for database
   ✓ Increase GPU memory to 256MB
   ✓ Monitor system temperature (< 80°C)
   ✓ Run in headless mode on Pi

3. SECURITY
   ✓ Backup database daily
   ✓ Enable authentication for admin functions
   ✓ Log all unknown faces for auditing
   ✓ Restrict file permissions on database
   ✓ Use HTTPS if web interface added
   ✓ Anonymize sensitive data in reports

4. RELIABILITY
   ✓ Test camera on startup
   ✓ Handle graceful shutdown
   ✓ Implement error recovery
   ✓ Use try-catch for database operations
   ✓ Regular backups (hourly during operation)
   ✓ Monitor system logs for errors

5. MAINTENANCE
   ✓ Clean unknown_faces table weekly
   ✓ Archive old attendance data monthly
   ✓ Test face detection accuracy monthly
   ✓ Update libraries quarterly
   ✓ Check database integrity weekly
   ✓ Review system logs regularly

6. DEPLOYMENT
   ✓ Test on target hardware first
   ✓ Start with small student set (10-20)
   ✓ Gradually increase to full class
   ✓ Have manual backup attendance method
   ✓ Train staff on system usage
   ✓ Document any customizations

7. TROUBLESHOOTING
   ✓ Check camera connection first
   ✓ Verify Python environment
   ✓ Test individual components
   ✓ Check system resources (CPU, memory)
   ✓ Review database logs
   ✓ Test face detection with sample images
"""


# ============================================================================
# CONFIGURATION PROFILES BY USE CASE
# ============================================================================

class UseCaseProfiles:
    """Pre-configured profiles for different scenarios"""
    
    # University Large Lecture (200+ students)
    LARGE_LECTURE = {
        'description': 'Large lecture hall with multiple entries',
        'camera_config': CameraConfig.OUTDOOR,
        'database_config': DatabaseConfig.HIGH_VOLUME,
        'face_config': FaceRecognitionConfig.LENIENT,
        'performance_profile': PerformanceProfile.PC_HIGH_QUALITY,
        'notes': [
            'Use multiple cameras at different entrances',
            'Higher debounce time to prevent duplicates',
            'Export reports after each class',
            'Archive data weekly'
        ]
    }
    
    # Lab Session (20-30 students)
    LAB_SESSION = {
        'description': 'Laboratory session with controlled environment',
        'camera_config': CameraConfig.PI_USB_CAMERA,
        'database_config': DatabaseConfig.STANDARD,
        'face_config': FaceRecognitionConfig.SECURITY,
        'performance_profile': PerformanceProfile.PI4_BALANCED,
        'notes': [
            'Log unknown persons for security',
            'Verify authorized personnel only',
            'Keep detailed audit trail',
            'Review logs at session end'
        ]
    }
    
    # Exam Hall (50-100 students)
    EXAM_HALL = {
        'description': 'Exam proctoring and verification',
        'camera_config': CameraConfig.PI_CSI_CAMERA,
        'database_config': DatabaseConfig.STANDARD,
        'face_config': FaceRecognitionConfig.STRICT,
        'performance_profile': PerformanceProfile.PI5_HIGH_QUALITY,
        'notes': [
            'High detection confidence for strict verification',
            'Log all detections for audit',
            'Manual verification for rejections',
            'Secure all records'
        ]
    }
    
    # Remote/Low-Power (Internet connectivity limited)
    LOW_POWER = {
        'description': 'Outdoor or battery-powered operation',
        'camera_config': CameraConfig.LAPTOP_LOW_POWER,
        'database_config': DatabaseConfig.STANDARD,
        'face_config': FaceRecognitionConfig.BALANCED,
        'performance_profile': PerformanceProfile.PI4_MAX_PERFORMANCE,
        'notes': [
            'Minimize power consumption',
            'Local database only',
            'Sync when power available',
            'Reduce frame resolution'
        ]
    }


# ============================================================================
# MONITORING & ALERTING TEMPLATES
# ============================================================================

class MonitoringAlerts:
    """Alert thresholds and monitoring templates"""
    
    # System Health Alerts
    CPU_THRESHOLD = 80          # Alert if CPU > 80%
    MEMORY_THRESHOLD = 90       # Alert if Memory > 90%
    TEMP_THRESHOLD = 80         # Alert if Temp > 80°C (Pi)
    
    # Face Detection Alerts
    LOW_CONFIDENCE_THRESHOLD = 0.3
    UNKNOWN_FACE_THRESHOLD = 10  # Alert if 10+ unknown faces in session
    
    # Database Alerts
    DATABASE_SIZE_THRESHOLD = 500  # MB
    SYNC_FAILURE_THRESHOLD = 3     # Consecutive failures
    
    @staticmethod
    def check_system_health():
        """Example health check function"""
        import psutil
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        
        alerts = []
        
        if cpu > MonitoringAlerts.CPU_THRESHOLD:
            alerts.append(f"CPU HIGH: {cpu}%")
        
        if memory > MonitoringAlerts.MEMORY_THRESHOLD:
            alerts.append(f"MEMORY HIGH: {memory}%")
        
        return alerts


# ============================================================================
# QUICK SETUP TEMPLATES
# ============================================================================

"""
QUICK SETUP FOR DIFFERENT SCENARIOS

1. RASPBERRY PI CLASSROOM:
   $ python3 attendance_system.py --headless
   
   Key Settings:
   - Scale Factor: 0.5
   - Debounce: 60 seconds
   - Detection Confidence: 0.5

2. DESKTOP COMPUTER:
   $ python3 attendance_system.py
   
   Key Settings:
   - Scale Factor: 1.0 (no scaling)
   - Debounce: 60 seconds
   - Detection Confidence: 0.7

3. SECURITY-FOCUSED LAB:
   - Detection Confidence: 0.8
   - Tolerance: 30.0
   - Log unknown faces
   - Enable audit trail

4. HIGH-VOLUME AUDITORIUM:
   - Multiple cameras
   - Lenient tolerance: 50.0
   - Batch database writes
   - Archive daily
"""

# ============================================================================
# TROUBLESHOOTING CONFIGURATIONS
# ============================================================================

class TroubleshootingConfigs:
    """Configurations for troubleshooting common issues"""
    
    # Issue: Low FPS
    LOW_FPS_FIX = {
        'frame_scale_factor': 0.25,
        'queue_size': 1,
        'detection_confidence': 0.3,
        'headless_mode': True,
    }
    
    # Issue: Many False Positives
    FALSE_POSITIVE_FIX = {
        'detection_confidence': 0.8,
        'recognition_tolerance': 30.0,
        'debounce_seconds': 120,
    }
    
    # Issue: Missed Detections
    MISSED_DETECTION_FIX = {
        'detection_confidence': 0.3,
        'recognition_tolerance': 50.0,
        'frame_scale_factor': 1.0,
    }
    
    # Issue: Out of Memory
    MEMORY_FIX = {
        'frame_scale_factor': 0.25,
        'queue_size': 1,
        'disable_unknown_face_logging': True,
        'batch_process': True,
    }

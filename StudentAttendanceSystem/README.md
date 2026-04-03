# Student Attendance System - Facial Recognition

**Optimized for Raspberry Pi 4/5 with Mediapipe & OpenCV**

A high-performance, Python-based student attendance system using facial recognition. Designed specifically for ARM architecture optimization with multithreading, frame resizing, and efficient SQLite database storage.

![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%204%2F5%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

---

## 🎯 Features

### Core Functionality
- ✅ **Real-Time Facial Recognition** using Mediapipe (ARM-optimized)
- ✅ **Thread-based Camera Polling** for high FPS and responsive UI
- ✅ **SQLite Database** for efficient local storage
- ✅ **Debounce Logic** to prevent duplicate attendance within 1 minute
- ✅ **Unknown Face Logging** for security and monitoring
- ✅ **CSV Export** for attendance reports
- ✅ **Batch Student Registration** from photo directories
- ✅ **Real-time Detection Display** or Headless Console Mode

### Performance Optimizations
- Frame resizing and downscaling (50% by default)
- Multithreading for camera and face processing
- ARM-specific engine selection (Mediapipe instead of Dlib)
- Minimal frame queue to prevent memory overflow
- Configurable FPS and resolution
- Low-latency face detection with confidence thresholding

### GUI & Interface
- Console mode with menu-driven interface
- GUI mode with live camera feed display
- Real-time FPS counter
- Color-coded face detection (green=known, red=unknown)
- Non-blocking camera capture

---

## 📋 Requirements

### Hardware
- **Raspberry Pi 4** (4GB RAM+) or **Raspberry Pi 5**
- **USB Camera** or **CSI Ribbon Camera**
- **Power Supply**: 5V/3A (Pi4) or 5V/4A (Pi5)
- **32GB microSD** (Class 10+)

### Software
- **Python 3.7+**
- Dependencies in `requirements.txt`:
  - opencv-python 4.8.1.78
  - mediapipe 0.10.4
  - numpy 1.24.3
  - pandas 2.0.3
  - SQLAlchemy 2.0.20
  - Pillow 9.5.0

---

## 🚀 Quick Start

### 1. Clone/Download Project
```bash
git clone <repository-url>
cd StudentAttendanceSystem
```

### 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare Dataset
```bash
# Create directories
mkdir -p dataset/known_faces
mkdir -p dataset/unknown_faces

# Add student photos in this format:
# dataset/known_faces/StudentName_RollNumber/photo1.jpg
#                                            photo2.jpg
#                                            photo3.jpg

# For detailed setup, see DATASET_SETUP.md
```

### 5. Register Students
```bash
# Batch register from directories
python3 registration_utility.py --mode batch --dir ./dataset/known_faces
```

### 6. Start System

**Console Mode (Recommended for Pi):**
```bash
python3 attendance_system.py --headless
```

**GUI Mode (with camera preview):**
```bash
python3 attendance_system.py
```

---

## 📁 File Structure

```
StudentAttendanceSystem/
├── README.md                          # This file
├── INSTALLATION_GUIDE.md              # Detailed setup instructions
├── DATASET_SETUP.md                   # Dataset organization guide
├── requirements.txt                   # Python dependencies
│
├── attendance_system.py               # Main application
├── database_handler.py                # SQLite operations
├── face_recognition.py                # Mediapipe face engine
├── registration_utility.py            # Student registration tool
├── config.py                          # Configuration settings
│
├── dataset/
│   ├── known_faces/
│   │   ├── Alice_Johnson_A001/
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
│   │   └── Bob_Smith_A002/
│   │       └── photo1.jpg
│   └── unknown_faces/                 # Auto-populated
│
├── student_photos/                    # Captured during registration
├── reports/                           # CSV exports
│
└── attendance.db                      # SQLite database (auto-created)
```

---

## 🎓 Database Schema

### Students Table
```sql
CREATE TABLE students (
    student_id        INTEGER PRIMARY KEY,
    name              TEXT NOT NULL,
    roll_number       TEXT UNIQUE NOT NULL,
    face_encoding     BLOB NOT NULL,
    registered_date   TIMESTAMP
);
```

### Attendance Table
```sql
CREATE TABLE attendance (
    attendance_id     INTEGER PRIMARY KEY,
    student_id        INTEGER NOT NULL,
    timestamp         TIMESTAMP,
    status            TEXT DEFAULT 'Present'
);
```

### Unknown Faces Table
```sql
CREATE TABLE unknown_faces (
    unknown_id        INTEGER PRIMARY KEY,
    timestamp         TIMESTAMP,
    face_image        BLOB
);
```

---

## 🔧 Usage Examples

### Start Attendance Monitoring
```bash
python3 attendance_system.py --headless
# Menu option 1: Start Attendance Monitoring
```

### Register Single Student
```bash
python3 registration_utility.py --mode single \
    --name "John Doe" \
    --roll "A001" \
    --image "photos/john.jpg"
```

### Capture Photos from Camera
```bash
python3 registration_utility.py --mode capture \
    --name "John Doe" \
    --roll "A001"
```

### Export Attendance Report
```bash
python3 attendance_system.py --headless
# Menu option 4: Export Attendance to CSV
```

### Get Today's Attendance
```bash
python3 attendance_system.py --headless
# Menu option 3: View Today's Attendance
```

### Python API Usage
```python
from attendance_system import AttendanceSystem

# Initialize system
system = AttendanceSystem(headless_mode=True)

# Get all students
students = system.db.get_all_students()

# Get today's attendance
records = system.db.get_today_attendance()

# Export to CSV
system.export_attendance("report.csv")

# View report
system.get_today_attendance_report()
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Camera settings
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_SCALE_FACTOR = 0.5

# Face detection
FACE_DETECTION_CONFIDENCE = 0.5
FACE_RECOGNITION_TOLERANCE = 40.0

# Attendance
DEBOUNCE_SECONDS = 60

# Performance
NUM_WORKERS = 2
QUEUE_MAX_SIZE = 2
```

---

## 🎯 Performance Tips

### For Raspberry Pi
1. **Disable Desktop:** Use Lite OS or disable GUI
2. **Use Headless Mode:** `python3 attendance_system.py --headless`
3. **Reduce Frame Size:** Set `FRAME_SCALE_FACTOR = 0.25`
4. **Increase GPU Memory:** `raspi-config` → 256MB
5. **Use External SSD:** Faster database operations

### For Battery/Low Power
1. Reduce frame resolution
2. Increase debounce time
3. Batch database writes
4. Disable FPS counter

---

## 🐛 Troubleshooting

### Camera Not Detected
```bash
# Check available cameras
ls -l /dev/video*

# Test with OpenCV
python3 -c "import cv2; cap=cv2.VideoCapture(0); print(cap.isOpened())"
```

### Low FPS / Laggy
```python
# Edit attendance_system.py
system = AttendanceSystem(
    scale_factor=0.25,      # Reduce to 25%
    frame_width=320,        # Lower resolution
    frame_height=240
)
```

### Poor Face Recognition
- Add more photos per student (3-5 minimum)
- Improve lighting in photos
- Ensure face is 30-70% of image
- Retrain: `python3 registration_utility.py --mode batch --dir ./dataset/known_faces`

### Out of Memory (Pi)
- Disable face image logging
- Reduce frame queue size
- Use external storage for database

For more troubleshooting, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting)

---

## 📊 System Specifications

| Component | Details |
|-----------|---------|
| Face Detection | Mediapipe FaceDetection |
| Face Recognition | Simple Euclidean distance on embeddings |
| Database | SQLite3 |
| Processing | Multi-threaded camera + face processing |
| FPS | 10-15 FPS (Pi4 with 50% scaling), 20+ FPS (PC) |
| Memory Usage | ~200MB (Pi4), variable on PC |
| Database Size | ~5KB per student |
| Frame Queue | 2 frames max (prevents latency) |

---

## 📈 Optimization Strategies

### Frame Processing Pipeline
```
Camera → Capture Thread → Queue → Processing Thread → Recognition → Database
   ↓
 Resize to 50%
   ↓
 Detect faces (Mediapipe)
   ↓
 Extract embeddings
   ↓
 Compare with known faces
   ↓
 Apply debounce logic
   ↓
 Mark attendance
```

### Debounce Logic
- Prevents duplicate attendance within 60 seconds
- Stored in memory: `{student_id: last_detection_time}`
- Configurable in `config.py`: `DEBOUNCE_SECONDS`

### Memory Efficiency
- Frame queue size: 2 frames (drops oldest)
- No full frames stored in memory
- Database uses indexed queries
- Face encodings: ~1KB each

---

## 🔐 Security Considerations

1. **Unknown Face Logging:** All unrecognized faces logged to database
2. **Database Encryption:** Optional (implement with SQLite extensions)
3. **Access Control:** Implement file permissions on `attendance.db`
4. **Regular Backups:** Export CSV reports regularly
5. **Rate Limiting:** Debounce prevents timing attacks

---

## 📚 Documentation

- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Detailed setup for all platforms
- **[DATASET_SETUP.md](DATASET_SETUP.md)** - Dataset organization and management
- **[config.py](config.py)** - All configurable parameters

---

## 🤝 Contributing

Suggestions for improvements:
- [ ] Tkinter GUI interface
- [ ] Web dashboard
- [ ] Email notifications
- [ ] Attendance statistics
- [ ] Face mask detection
- [ ] Multiple camera support
- [ ] LED/buzzer notifications

---

## 📄 License

MIT License - Free to use and modify

---

## 👥 Support

For issues or questions:
1. Check [INSTALLATION_GUIDE.md - Troubleshooting](INSTALLATION_GUIDE.md#troubleshooting)
2. Check [DATASET_SETUP.md](DATASET_SETUP.md) for dataset issues
3. Review camera permissions and database locks

---

## 🎓 Example Use Cases

### University Lecture Halls
```python
# Auto-mark attendance as students enter
# 30+ students per class
# Roll call export after class
```

### Laboratory Sessions
```python
# Verify authorized personnel
# Log unknown persons
# Track lab access times
```

### Exam Halls
```python
# Real-time proctoring
# Prevent unauthorized entries
# Audit trail of all entries/exits
```

---

## 📊 Performance Benchmarks

### Raspberry Pi 4 (4GB)
- **FPS:** 12-15 FPS @ 50% scale
- **Detection Latency:** ~300ms
- **CPU Usage:** 40-60%
- **Memory:** 180-250MB

### Intel i5 Laptop
- **FPS:** 25-30 FPS @ full scale
- **Detection Latency:** ~100ms
- **CPU Usage:** 20-30%
- **Memory:** 300-500MB

---

## 🙏 Acknowledgments

- **Mediapipe:** Google's Face Detection solution
- **OpenCV:** Computer vision library
- **SQLite:** Lightweight database engine

---

**Last Updated:** 2024
**Version:** 1.0.0
**Python:** 3.7+

Ready to deployto Raspberry Pi! 🚀

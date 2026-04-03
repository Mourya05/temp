# Student Attendance System - Installation & Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation on Raspberry Pi](#installation-on-raspberry-pi)
3. [Installation on Linux/macOS](#installation-on-linuxmacos)
4. [Installation on Windows](#installation-on-windows)
5. [Dataset Setup](#dataset-setup)
6. [Running the System](#running-the-system)
7. [Troubleshooting](#troubleshooting)
8. [Performance Optimization Tips](#performance-optimization-tips)

---

## System Requirements

### Hardware (Raspberry Pi)
- **Raspberry Pi 4** (4GB RAM minimum, 8GB recommended) or **Raspberry Pi 5**
- **32GB microSD card** (Class 10 recommended)
- **USB Camera** (or CSI camera ribbon cable)
- **5V/3A Power Supply** for Raspberry Pi 4
- **5V/4A Power Supply** for Raspberry Pi 5
- Optional: **External SSD** for faster database operations

### Hardware (PC/Laptop)
- **Intel Core i5** or equivalent processor
- **4GB RAM minimum**
- **USB Webcam**
- **Windows 10+, Ubuntu 18.04+, or macOS 10.14+**

### Software Requirements
- **Python 3.7+**
- **pip** (Python package manager)
- **virtualenv** or **conda** (recommended)

---

## Installation on Raspberry Pi

### Step 1: Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv python3-dev
sudo apt-get install -y libatlas-base-dev libjasper-dev libtiff5 libjasper1 libharfbuzz0b libwebp6
sudo apt-get install -y libopenjp2-7 libtiff5 libharfbuzz0b libwebp6 -y
sudo apt-get install -y build-essential cmake pkg-config
```

### Step 2: Create Project Directory
```bash
mkdir -p ~/projects/attendance_system
cd ~/projects/attendance_system
```

### Step 3: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

On Raspberry Pi with 32-bit OS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**For Raspberry Pi 32-bit**, use pre-compiled wheels:
```bash
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.4
pip install numpy==1.24.3
pip install pandas==2.0.3
```

### Step 5: Enable Camera
If using USB camera:
```bash
# Camera should auto-detect
# Test with: python3 -c "import cv2; print(cv2.__version__)"
```

If using CSI camera (ribbon cable):
```bash
sudo raspi-config
# Navigate to: Interfacing Options > Camera > Enable
# Reboot: sudo reboot
```

### Step 6: Verify Installation
```bash
python3 -c "import cv2; import mediapipe; print('OpenCV:', cv2.__version__); print('Mediapipe: OK')"
```

---

## Installation on Linux/macOS

### Step 1: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
sudo apt-get install -y libopencv-dev python3-opencv
sudo apt-get install -y libsm6 libxext6 libxrender-dev
```

**macOS:**
```bash
brew install python3
brew install opencv
```

### Step 2: Create Virtual Environment
```bash
mkdir -p ~/projects/attendance_system
cd ~/projects/attendance_system
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python3 -c "import cv2; import mediapipe; print('Installation successful')"
```

---

## Installation on Windows

### Step 1: Install Python
- Download Python 3.9+ from https://www.python.org/downloads/
- **Important:** Check "Add Python to PATH" during installation
- Verify: Open PowerShell and run `python --version`

### Step 2: Create Project Directory
```powershell
mkdir C:\AttendanceSystem
cd C:\AttendanceSystem
```

### Step 3: Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies
```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Step 5: Connect USB Camera
- Plug in USB camera
- Windows should auto-install drivers
- Test availability in Python

### Step 6: Verify Installation
```powershell
python -c "import cv2; import mediapipe; print('Installation successful')"
```

---

## Dataset Setup

### Directory Structure

Create the following directory structure for student images:

```
StudentAttendanceSystem/
├── dataset/
│   ├── known_faces/
│   │   ├── John_Smith_A001/
│   │   │   ├── photo1.jpg
│   │   │   ├── photo2.jpg
│   │   │   └── photo3.jpg
│   │   ├── Jane_Doe_A002/
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
│   │   └── ...
│   └── unknown_faces/
│       └── (auto-populated during runtime)
├── student_photos/
│   └── (captured photos from camera)
└── reports/
    └── (exported CSV reports)
```

### Directory Naming Convention

The directory name format is: **StudentName_RollNumber**

Examples:
- `John_Smith_A001`
- `Jane_Doe_A002`
- `Alice_Johnson_CSE401`

**Important:** Use underscores `_` to separate name and roll number, no spaces.

### Adding Student Photos

**Method 1: Manually Add Photos**

1. Create a folder: `dataset/known_faces/StudentName_RollNumber/`
2. Add photos of the student (JPG or PNG format)
3. Ensure clear face visibility
4. Use 3-5 photos per student at different angles

**Method 2: Batch Register from Directory**

```bash
python3 registration_utility.py --mode batch --dir ./dataset/known_faces
```

**Method 3: Register Single Student with Photo**

```bash
python3 registration_utility.py --mode single \
    --name "John Smith" \
    --roll "A001" \
    --image "/path/to/photo.jpg"
```

**Method 4: Capture Photos from Camera**

```bash
python3 registration_utility.py --mode capture \
    --name "John Smith" \
    --roll "A001"
```

### Photo Requirements

- **Format:** JPG, PNG
- **Resolution:** 480x640 or higher
- **Face Size:** Face should occupy 30-70% of the image
- **Lighting:** Adequate lighting, no shadows on face
- **Angle:** Front-facing, slight side angles (±20°)
- **Quantity:** 3-5 photos per student recommended
- **Background:** Plain or natural background (avoid busy backgrounds)

---

## Running the System

### Quick Start (Headless Mode - Console)

```bash
source venv/bin/activate  # Activate virtual environment
python3 attendance_system.py --headless
```

This opens an interactive menu where you can:
1. Start attendance monitoring
2. Register new students
3. View today's attendance
4. Export attendance to CSV
5. Delete student records

### GUI Mode (with OpenCV Display)

```bash
python3 attendance_system.py
```

This shows:
- Live camera feed
- Detected faces with bounding boxes
- Real-time detection results
- FPS counter

**Controls:**
- Press `q` to quit

### Register Students

**Option 1: Batch Import**
```bash
python3 registration_utility.py --mode batch --dir ./dataset/known_faces
```

**Option 2: Single Student**
```bash
python3 registration_utility.py --mode single \
    --name "John Smith" --roll "A001" --image "./photo.jpg"
```

**Option 3: Camera Capture**
```bash
python3 registration_utility.py --mode capture \
    --name "John Smith" --roll "A001"
```

### Export Attendance Reports

**From Python:**
```python
from attendance_system import AttendanceSystem
system = AttendanceSystem()
system.export_attendance("attendance_report.csv")
system.get_today_attendance_report()
```

**From Menu:**
- Run: `python3 attendance_system.py --headless`
- Select option 4: "Export Attendance to CSV"

---

## Troubleshooting

### Issue 1: Camera Not Detected

**Symptoms:** "Could not open camera" error

**Solutions:**
```bash
# List available video devices
ls -l /dev/video*

# Check USB camera connection
lsusb

# Try different camera ID
python3 -c "import cv2; cap=cv2.VideoCapture(1); print(cap.isOpened())"
```

Update `camera_id` in `attendance_system.py`:
```python
system = AttendanceSystem(camera_id=1)  # Try 1, 2, etc.
```

### Issue 2: Low FPS / Laggy Performance

**Symptoms:** Slow detection, freezing

**Solutions:**

1. **Enable Frame Downscaling:**
   Edit `attendance_system.py`:
   ```python
   system = AttendanceSystem(scale_factor=0.25)  # 25% of original size
   ```

2. **Reduce Resolution:**
   ```python
   system = AttendanceSystem(frame_width=320, frame_height=240)
   ```

3. **Check System Resources:**
   ```bash
   # Raspberry Pi
   top -bn1 | head -n 15  # CPU/Memory usage
   vcgencmd measure_temp   # Temperature
   ```

4. **Disable GUI:**
   ```bash
   python3 attendance_system.py --headless
   ```

### Issue 3: Poor Face Recognition

**Symptoms:** Students not recognized, many "Unknown" detections

**Solutions:**

1. **Improve Photo Quality:**
   - Ensure better lighting in photos
   - Use 5+ photos instead of 1
   - Capture at different angles

2. **Adjust Tolerance:**
   ```python
   student_id, name, conf = face_engine.recognize_face(embedding, tolerance=50.0)
   ```

3. **Re-register Students:**
   ```bash
   python3 registration_utility.py --mode batch --dir ./dataset/known_faces
   ```

### Issue 4: Database Locked / Permission Errors

**Symptoms:** "database is locked" error

**Solutions:**
```bash
# Delete and recreate database
rm attendance.db
python3 attendance_system.py --headless
```

### Issue 5: Memory Issues on Raspberry Pi

**Symptoms:** Process crashes, "Killed" message

**Solutions:**

1. **Reduce Frame Queue:**
   Edit `attendance_system.py` line 56:
   ```python
   self.frame_queue = Queue(maxsize=1)
   ```

2. **Disable Face Logging:**
   Comment out in `face_recognition.py`:
   ```python
   # self.db.log_unknown_face()
   ```

3. **Use External Storage:**
   Move database to SSD:
   ```python
   system = AttendanceSystem(db_path="/mnt/ssd/attendance.db")
   ```

### Issue 6: ImportError for Mediapipe

**Symptoms:** "No module named 'mediapipe'" on Raspberry Pi

**Solution for Pi 32-bit:**
```bash
deactivate  # Exit venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Install pre-built packages
pip install --index-url https://www.piwheels.org/simple mediapipe
pip install -r requirements.txt
```

---

## Performance Optimization Tips

### For Raspberry Pi 4/5

1. **Disable Desktop Environment:**
   ```bash
   sudo raspi-config
   # System Options > Boot / Auto Login > Desktop disabled
   ```

2. **Increase GPU Memory:**
   ```bash
   sudo raspi-config
   # Advanced Options > GPU Memory > 256MB
   ```

3. **Optimize System Clock:**
   ```bash
   sudo nano /boot/config.txt
   # Add: arm_freq=2000
   sudo reboot
   ```

4. **Run on Lightweight OS:**
   Use DietPi or PiCore for minimal overhead

5. **Database Optimization:**
   ```python
   # Enable WAL mode for faster I/O
   conn.execute("PRAGMA journal_mode=WAL")
   ```

6. **Thread Priority:**
   Run with higher priority:
   ```bash
   nice -n -10 python3 attendance_system.py
   ```

### General Optimization

- Use `--headless` mode (skips GUI rendering)
- Reduce frame resolution and scale factor
- Increase debounce time to reduce database writes
- Use external storage (SSD via USB)
- Enable face detection caching
- Batch process database inserts

---

## File Structure

```
StudentAttendanceSystem/
├── README.md                    (This file)
├── requirements.txt             (Python dependencies)
├── config.py                    (Configuration settings)
├── attendance_system.py          (Main system file)
├── database_handler.py          (SQLite database operations)
├── face_recognition.py          (Face detection/recognition engine)
├── registration_utility.py      (Student registration tool)
├── attendance.db                (SQLite database - auto-created)
├── dataset/
│   ├── known_faces/
│   │   └── StudentName_RollNumber/
│   │       └── photo.jpg
│   └── unknown_faces/
├── student_photos/              (Captured during registration)
└── reports/                     (CSV exports)
```

---

## Command Reference

```bash
# Activate environment
source venv/bin/activate        # Linux/macOS
venv\Scripts\Activate.ps1       # Windows PowerShell

# Quick start
python3 attendance_system.py --headless

# GUI mode
python3 attendance_system.py

# Batch register
python3 registration_utility.py --mode batch --dir ./dataset/known_faces

# Single register
python3 registration_utility.py --mode single --name "John" --roll "A001" --image "photo.jpg"

# Camera capture
python3 registration_utility.py --mode capture --name "John" --roll "A001"
```

---

## Support & Troubleshooting

- Check camera permissions: `ls -l /dev/video*`
- Verify database: `sqlite3 attendance.db ".tables"`
- Check logs: `tail -f attendance_system.log`
- Test Mediapipe: `python3 -m mediapipe.examples.python.pose_landmarker`

Happy Attendance Tracking! 🎓

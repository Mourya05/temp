# Terminal Commands - Student Attendance System

Quick copy-paste terminal commands for setup and usage.

---

## 🖥️ RASPBERRY PI 4/5 SETUP

### Initial System Setup
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv python3-dev
sudo apt-get install -y libatlas-base-dev libjasper-dev libtiff5 libjasper1
sudo apt-get install -y libharfbuzz0b libwebp6 libopenjp2-7
sudo apt-get install -y build-essential cmake pkg-config
```

### Project Setup
```bash
mkdir -p ~/projects/attendance_system
cd ~/projects/attendance_system
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Enable Camera (if using CSI/Ribbon)
```bash
sudo raspi-config
# Interfacing Options > Camera > Enable
# Then reboot
sudo reboot
```

### Verify Installation
```bash
python3 -c "import cv2; import mediapipe; print('✓ Installation successful')"
```

---

## 🐧 UBUNTU/DEBIAN LINUX SETUP

### Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
sudo apt-get install -y libopencv-dev python3-opencv
sudo apt-get install -y libsm6 libxext6 libxrender-dev
```

### Project Setup
```bash
mkdir -p ~/projects/attendance_system
cd ~/projects/attendance_system
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Verify Installation
```bash
python3 -c "import cv2; import mediapipe; print('✓ Installation successful')"
```

---

## 🍎 MACOS SETUP

### Install Homebrew and Python
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
brew install opencv
brew install cmake
```

### Project Setup
```bash
mkdir -p ~/projects/attendance_system
cd ~/projects/attendance_system
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Verify Installation
```bash
python3 -c "import cv2; import mediapipe; print('✓ Installation successful')"
```

---

## 🪟 WINDOWS SETUP

### Install Python (PowerShell as Administrator)
```powershell
# Download and run Python installer from python.org
# Make sure to check "Add Python to PATH"
python --version
```

### Project Setup
```powershell
mkdir C:\AttendanceSystem
cd C:\AttendanceSystem
python -m venv venv
venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Verify Installation
```powershell
python -c "import cv2; import mediapipe; print('✓ Installation successful')"
```

---

## 📁 DATASET SETUP

### Create Directory Structure
```bash
# Linux/macOS
mkdir -p dataset/known_faces
mkdir -p dataset/unknown_faces
mkdir -p reports
mkdir -p student_photos

# Windows PowerShell
New-Item -ItemType Directory -Path "dataset\known_faces"
New-Item -ItemType Directory -Path "dataset\unknown_faces"
New-Item -ItemType Directory -Path "reports"
New-Item -ItemType Directory -Path "student_photos"
```

### Create Student Directories (Linux/macOS)
```bash
cd dataset/known_faces

# Create multiple student directories
mkdir Alice_Johnson_A001
mkdir Bob_Smith_A002
mkdir Charlie_Brown_A003
mkdir Diana_Chen_A004
mkdir Eve_Williams_A005

# Copy photos
cp ~/photos/alice*.jpg Alice_Johnson_A001/
cp ~/photos/bob*.jpg Bob_Smith_A002/
cp ~/photos/charlie*.jpg Charlie_Brown_A003/
```

### Create Student Directories (Windows PowerShell)
```powershell
cd dataset\known_faces

$students = @(
    'Alice_Johnson_A001',
    'Bob_Smith_A002',
    'Charlie_Brown_A003',
    'Diana_Chen_A004',
    'Eve_Williams_A005'
)

foreach ($student in $students) {
    New-Item -ItemType Directory -Path $student -Force
    Write-Host "Created: $student"
}
```

### Bulk Create from CSV (Linux/macOS)
```bash
# Create students.csv with format: FirstName,LastName,RollNumber
# Alice,Johnson,A001
# Bob,Smith,A002

while IFS=',' read -r first last roll; do
    mkdir -p "dataset/known_faces/${first}_${last}_${roll}"
done < students.csv
```

### Bulk Create from CSV (Windows PowerShell)
```powershell
$students = Import-Csv -Path "students.csv"
foreach ($student in $students) {
    $dir = "dataset\known_faces\$($student.FirstName)_$($student.LastName)_$($student.RollNumber)"
    New-Item -ItemType Directory -Path $dir -Force
}
```

---

## 👥 STUDENT REGISTRATION

### Batch Register from Directory
```bash
python3 registration_utility.py --mode batch --dir ./dataset/known_faces
```

### Register Single Student
```bash
python3 registration_utility.py --mode single \
    --name "John Doe" \
    --roll "A001" \
    --image "/path/to/photo.jpg"
```

### Capture Photos from Camera
```bash
python3 registration_utility.py --mode capture \
    --name "John Doe" \
    --roll "A001"
```

### Register Multiple Students (Bash Loop)
```bash
# Create students.csv: Name,RollNumber,PhotoPath
# John Doe,A001,photos/john.jpg
# Jane Smith,A002,photos/jane.jpg

while IFS=',' read -r name roll photo; do
    python3 registration_utility.py --mode single \
        --name "$name" --roll "$roll" --image "$photo"
done < students.csv
```

---

## ▶️ RUN ATTENDANCE SYSTEM

### Headless Mode (Console / Recommended for Pi)
```bash
python3 attendance_system.py --headless
```

### GUI Mode (with Camera Preview)
```bash
python3 attendance_system.py
```

### Run in Background (Linux/macOS)
```bash
# Start in background
nohup python3 attendance_system.py --headless > attendance.log 2>&1 &

# Get PID
ps aux | grep attendance_system.py

# Kill process
kill <PID>
```

### Run in Background (Windows PowerShell)
```powershell
# Start in background
Start-Process python -ArgumentList "attendance_system.py --headless" -WindowStyle Hidden

# List running Python processes
Get-Process python

# Kill process
Stop-Process -Name python -Force
```

### Run with Higher Priority (Linux/macOS)
```bash
nice -n -10 python3 attendance_system.py --headless
```

---

## 📊 ATTENDANCE OPERATIONS

### Export Today's Attendance
```bash
python3 attendance_system.py --headless
# Select option 4: Export Attendance to CSV
```

### Export with Specific Filename
```python
python3 << 'EOF'
from attendance_system import AttendanceSystem
system = AttendanceSystem()
system.export_attendance("attendance_2024_01_15.csv")
system.get_today_attendance_report()
EOF
```

### View Database Records (SQL)
```bash
# Open SQLite database
sqlite3 attendance.db

# View all students
SELECT student_id, name, roll_number FROM students;

# View today's attendance
SELECT s.name, s.roll_number, COUNT(*) 
FROM attendance a 
JOIN students s ON a.student_id = s.student_id 
WHERE DATE(a.timestamp) = DATE('now')
GROUP BY a.student_id;

# Exit SQLite
.quit
```

### Backup Database
```bash
# Linux/macOS
cp attendance.db attendance_backup_$(date +%Y%m%d_%H%M%S).db

# Windows PowerShell
Copy-Item "attendance.db" "attendance_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

### Delete Old Records (Keep last 30 days)
```bash
sqlite3 attendance.db << 'EOF'
DELETE FROM attendance WHERE timestamp < datetime('now', '-30 days');
DELETE FROM unknown_faces WHERE timestamp < datetime('now', '-30 days');
VACUUM;
.quit
EOF
```

---

## 🔧 SYSTEM DIAGNOSTICS

### Check Camera Status
```bash
# Linux/macOS
ls -l /dev/video*
lsusb | grep -i camera

# Windows PowerShell
Get-PnpDevice | Where-Object {$_.Class -eq 'Camera'}
```

### Test Camera with OpenCV
```python
python3 << 'EOF'
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✓ Camera 0: OK")
    ret, frame = cap.read()
    print(f"✓ Frame size: {frame.shape}")
    cap.release()
else:
    print("✗ Camera 0: Failed")
EOF
```

### Check System Resources (Raspberry Pi)
```bash
# CPU and memory
top -bn1 | head -n 15

# Temperature
vcgencmd measure_temp

# Disk usage
df -h

# GPU memory
vcgencmd get_config gpu_mem
```

### Check System Resources (Linux)
```bash
# CPU and memory
free -h
top -bn1 | head -n 10

# Disk usage
df -h

# Process details
ps aux | grep python
```

### Check System Resources (macOS)
```bash
# Memory usage
vm_stat

# CPU usage
top -l 1 | head -20

# Disk usage
df -h
```

### Verify Database
```bash
# Check database integrity
sqlite3 attendance.db "PRAGMA integrity_check;"

# Get database statistics
sqlite3 attendance.db << 'EOF'
SELECT 'Students' as table_name, COUNT(*) as count FROM students
UNION ALL
SELECT 'Attendance', COUNT(*) FROM attendance
UNION ALL
SELECT 'Unknown Faces', COUNT(*) FROM unknown_faces;
.quit
EOF
```

---

## 📊 BATCH OPERATIONS

### Create Attendance Summary Report
```bash
python3 << 'EOF'
from attendance_system import AttendanceSystem
import pandas as pd

system = AttendanceSystem()

# Export today's attendance
records = system.db.get_today_attendance()
df = pd.DataFrame(records, columns=['Name', 'Roll', 'Count'])
df.to_csv('daily_summary.csv', index=False)

# Create statistics
print(f"Total Students: {len(df)}")
print(f"Present Today: {len(df[df['Count'] > 0])}")
print(f"Absent: {len(df[df['Count'] == 0])}")
EOF
```

### List All Registered Students
```bash
python3 << 'EOF'
from attendance_system import AttendanceSystem

system = AttendanceSystem()
students = system.db.get_all_students()

print(f"{'ID':<5} {'Name':<20} {'Roll Number':<15}")
print("-" * 40)
for student in students:
    print(f"{student[0]:<5} {student[1]:<20} {student[2]:<15}")
EOF
```

### Delete Student Record
```bash
python3 << 'EOF'
from attendance_system import AttendanceSystem

system = AttendanceSystem()
system.db.delete_student("A001")  # Replace with actual roll number
print("Student deleted successfully")
EOF
```

---

## 🔄 MAINTENANCE

### Clean Up Old Logs
```bash
# Linux/macOS
find . -name "*.log" -mtime +30 -delete

# Windows PowerShell
Get-ChildItem -Filter "*.log" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

### Optimize Database
```bash
sqlite3 attendance.db << 'EOF'
VACUUM;
ANALYZE;
.quit
EOF
```

### Reset System (Start Fresh)
```bash
# Backup first!
cp attendance.db attendance_db_backup.db

# Remove database
rm attendance.db

# Re-register students
python3 registration_utility.py --mode batch --dir ./dataset/known_faces
```

---

## 🆘 TROUBLESHOOTING COMMANDS

### Test Face Detection
```bash
python3 << 'EOF'
from face_recognition import FaceRecognitionEngine
engine = FaceRecognitionEngine()
embedding = engine.generate_embedding_from_image("dataset/known_faces/TestStudent/photo.jpg")
print(f"Face detected: {embedding is not None}")
EOF
```

### Check Camera Frames
```bash
python3 << 'EOF'
import cv2
import time

cap = cv2.VideoCapture(0)
frame_count = 0
start = time.time()

while frame_count < 30:
    ret, frame = cap.read()
    if ret:
        frame_count += 1

elapsed = time.time() - start
fps = frame_count / elapsed
print(f"FPS: {fps:.1f}")
cap.release()
EOF
```

### Validate Dataset
```bash
python3 << 'EOF'
import os
from face_recognition import FaceRecognitionEngine

engine = FaceRecognitionEngine()
dataset_dir = "dataset/known_faces"

for student_dir in os.listdir(dataset_dir):
    path = os.path.join(dataset_dir, student_dir)
    photos = [f for f in os.listdir(path) if f.endswith(('.jpg', '.png'))]
    
    if len(photos) < 3:
        print(f"⚠️  {student_dir}: Only {len(photos)} photos")
    else:
        print(f"✓ {student_dir}: {len(photos)} photos")
EOF
```

---

## 📝 NOTES

- Always activate virtual environment: `source venv/bin/activate`
- Use `--headless` mode on Raspberry Pi for better performance
- Backup database regularly: `cp attendance.db attendance_backup.db`
- Test camera before starting: `python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`
- For help: See README.md, INSTALLATION_GUIDE.md, or DATASET_SETUP.md

---

**Last Updated:** 2024
**Version:** 1.0

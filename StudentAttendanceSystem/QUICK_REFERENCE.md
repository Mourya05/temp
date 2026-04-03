# QUICK REFERENCE GUIDE
# For Student Attendance System - Facial Recognition

## 🚀 START HERE

### First Time Setup (5 minutes)
```bash
python3 -m venv venv
source venv/bin/activate        # On Pi/Linux
# venv\Scripts\Activate.ps1      # On Windows

pip install -r requirements.txt
```

### Run System
```bash
# On Raspberry Pi (headless):
python3 attendance_system.py --headless

# On Desktop (with GUI):
python3 attendance_system.py
```

---

## 📁 ESSENTIAL FILES

| File | Purpose |
|------|---------|
| `attendance_system.py` | 🎯 Main application |
| `database_handler.py` | 💾 Database operations |
| `face_recognition.py` | 👤 Face detection engine |
| `registration_utility.py` | 📝 Register students |
| `config.py` | ⚙️ Settings |

---

## 📚 DOCUMENTATION

| Document | Read This For |
|----------|---------------|
| `README.md` | Project overview |
| `INSTALLATION_GUIDE.md` | Setup instructions (choose your OS) |
| `DATASET_SETUP.md` | How to organize student photos |
| `TERMINAL_COMMANDS.md` | Copy-paste commands |
| `DELIVERABLES.md` | What you got |

---

## 🎯 COMMON TASKS

### 1. Register Students from Folder
```bash
python3 registration_utility.py --mode batch --dir ./dataset/known_faces
```

### 2. Register One Student
```bash
python3 registration_utility.py --mode single \
    --name "John Doe" --roll "A001" --image "photo.jpg"
```

### 3. Capture Photo from Camera
```bash
python3 registration_utility.py --mode capture \
    --name "John Doe" --roll "A001"
```

### 4. Export Attendance Report
Menu option from console interface, or:
```python
from attendance_system import AttendanceSystem
system = AttendanceSystem()
system.export_attendance("report.csv")
```

### 5. View Today's Report
From console menu or:
```python
system.get_today_attendance_report()
```

---

## ⚙️ BASIC CONFIGURATION

Edit `config.py` to customize:

```python
# Reduce for faster performance (Raspberry Pi)
FRAME_SCALE_FACTOR = 0.5        # Try 0.25 for slower hardware

# Change camera if needed
CAMERA_ID = 0                    # Try 1, 2 if 0 doesn't work

# Adjust detection sensitivity
FACE_DETECTION_CONFIDENCE = 0.5  # Higher = stricter (0.3-0.8)
FACE_RECOGNITION_TOLERANCE = 40.0  # Lower = stricter (30-50)

# Prevent duplicate entries
DEBOUNCE_SECONDS = 60            # Seconds between same student detections
```

---

## 📊 DATASET FOLDER STRUCTURE

```
dataset/known_faces/
├── FirstName_LastName_RollNumber/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
└── ...
```

**Key Points:**
- ✅ Use underscores: `Alice_Johnson_A001`
- ✅ 3-5 photos per student
- ✅ Clear face visibility
- ✅ Different angles (front, left, right)
- ✅ Good lighting

---

## 🆘 TROUBLESHOOTING QUICK FIX

### Camera Not Working
```bash
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
# Try different camera IDs: 1, 2, etc.
```

### Slow Performance
```python
# In attendance_system.py, increase scale_factor reduction:
system = AttendanceSystem(scale_factor=0.25)  # Was 0.5
```

### Poor Face Recognition
- Add more photos per student (use 5 instead of 3)
- Re-register: `python3 registration_utility.py --mode batch --dir ./dataset/known_faces`

### Unknown Faces Every Time
- Check lighting in photos
- Ensure face is centered and visible
- Try different camera angle

---

## 📈 EXPECTED PERFORMANCE

| Hardware | FPS | Quality |
|----------|-----|---------|
| Raspberry Pi 4 | 12-15 | Good ✅ |
| Raspberry Pi 5 | 18-22 | Excellent ✅ |
| Desktop PC | 25-30 | Excellent ✅ |

---

## 🔑 KEY FEATURES

✅ Mediapipe face detection (ARM-optimized)
✅ Thread-based camera polling (high FPS)
✅ SQLite database (local storage)
✅ CSV export (reporting)
✅ Console interface (easy to use)
✅ Debounce logic (prevent duplicates)
✅ Unknown face logging (security)

---

## 💾 DATABASE MANAGEMENT

### Check Database Status
```bash
sqlite3 attendance.db "SELECT COUNT(*) FROM students;" 
```

### View Today's Attendance
```bash
sqlite3 attendance.db "
SELECT s.name, COUNT(*) 
FROM attendance a 
JOIN students s ON a.student_id = s.student_id 
WHERE DATE(a.timestamp) = DATE('now')
GROUP BY a.student_id;"
```

### Backup Database
```bash
cp attendance.db attendance_backup_$(date +%Y%m%d).db
```

---

## 📝 FILE LOCATIONS

After first run, you'll have:

```
StudentAttendanceSystem/
├── attendance.db              ← Database (auto-created)
├── attendance_report.csv      ← Exported reports
├── dataset/
│   ├── known_faces/           ← Your student photos
│   └── unknown_faces/         ← Unknown detections
└── student_photos/            ← Captured during registration
```

---

## 🎓 QUICK RECIPES

### Recipe 1: Fast Setup for Small Class (10 students)
1. Create `dataset/known_faces/StudentName_Roll/` folders
2. Copy 3 photos per student
3. Run: `python3 registration_utility.py --mode batch --dir ./dataset/known_faces`
4. Run: `python3 attendance_system.py --headless`

### Recipe 2: Capture Photos & Register Live
```bash
python3 registration_utility.py --mode capture --name "John" --roll "A001"
```

### Recipe 3: Daily Attendance Workflow
1. Start: `python3 attendance_system.py --headless`
2. Select: "Start Attendance Monitoring"
3. After class, Select: "Export to CSV"
4. View: `attendance_report.csv`

---

## 📞 NEED HELP?

**Installation Issues:** → `INSTALLATION_GUIDE.md`
**Dataset Problems:** → `DATASET_SETUP.md`
**Commands:** → `TERMINAL_COMMANDS.md`
**Full Details:** → `README.md`
**What You Got:** → `DELIVERABLES.md`

---

## ✅ CHECKLIST BEFORE FIRST RUN

- [ ] Python 3.7+ installed
- [ ] Virtual environment activated
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] Dataset folder created: `dataset/known_faces/`
- [ ] Student photos added (3+ per student)
- [ ] Directory names correct: `FirstName_LastName_RollNumber`
- [ ] Camera tested and working
- [ ] Students registered: `python3 registration_utility.py --mode batch --dir ./dataset/known_faces`

✅ **Ready to Go!**

---

**Version:** 1.0
**Last Updated:** 2024
**Platform:** Raspberry Pi 4/5, Linux, macOS, Windows

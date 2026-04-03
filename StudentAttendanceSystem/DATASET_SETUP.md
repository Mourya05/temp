# Dataset Setup Guide for Student Attendance System

## Quick Start: Directory Structure

```
StudentAttendanceSystem/
├── dataset/
│   ├── known_faces/
│   │   ├── Alice_Johnson_2024CE001/
│   │   │   ├── photo1.jpg
│   │   │   ├── photo2.jpg
│   │   │   └── photo3.jpg
│   │   ├── Bob_Smith_2024CE002/
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
│   │   └── Charlie_Brown_2024CE003/
│   │       ├── photo1.jpg
│   │       ├── photo2.jpg
│   │       └── photo3.jpg
│   └── unknown_faces/
│       └── (Auto-populated during runtime)
└── reports/
    └── (CSV exports go here)
```

---

## Step-by-Step Setup

### Step 1: Create Directory Structure

**Linux/macOS:**
```bash
mkdir -p StudentAttendanceSystem/dataset/known_faces
mkdir -p StudentAttendanceSystem/dataset/unknown_faces
mkdir -p StudentAttendanceSystem/reports
```

**Windows PowerShell:**
```powershell
New-Item -ItemType Directory -Path "StudentAttendanceSystem\dataset\known_faces"
New-Item -ItemType Directory -Path "StudentAttendanceSystem\dataset\unknown_faces"
New-Item -ItemType Directory -Path "StudentAttendanceSystem\reports"
```

### Step 2: Naming Convention for Student Directories

**Format:** `FirstName_LastName_RollNumber`

**Rules:**
- Use underscores `_` to separate components
- No spaces in directory names
- No special characters except underscore
- Roll numbers can include letters (e.g., 2024CE001, A001, CSE-1A-001)

**Valid Examples:**
```
Alice_Johnson_2024CE001
Bob_Ahmed_A001
Charlie_Brown_CSE-1A-001
Diana_Chen_2024001
Eve_Williams_201
```

**Invalid Examples:**
```
Alice Johnson 2024CE001   ✗ (spaces)
Alice_Johnson_2024CE001   ✗ (would work, but prefer consistent naming)
Alice-Johnson-2024CE001   ✗ (hyphens - use underscores instead)
2024CE001                 ✗ (no name)
```

### Step 3: Add Student Photos

For each student directory, add 3-5 photos:

```bash
# Example: Add photos for Alice Johnson
cd StudentAttendanceSystem/dataset/known_faces/Alice_Johnson_2024CE001/
cp ~/Downloads/alice_photu1.jpg photo1.jpg
cp ~/Downloads/alice_photo2.jpg photo2.jpg
cp ~/Downloads/alice_photo3.jpg photo3.jpg
```

**Photo Naming Convention:**
- `photo1.jpg`, `photo2.jpg`, `photo3.jpg` (simple)
- Or: `face_front.jpg`, `face_left.jpg`, `face_right.jpg` (descriptive)

### Step 4: Photo Quality Guidelines

**Optimal Photo Characteristics:**

1. **Face Size in Image**
   - Face should occupy 30-70% of the image
   - Not too close, not too far

2. **Face Angles**
   - Front-facing (primary photo)
   - Left profile (-15° to -30°)
   - Right profile (+15° to +30°)
   - Top angle (-20°)
   - Bottom angle (+20°)

3. **Lighting Conditions**
   - Bright, even lighting
   - No harsh shadows on face
   - Natural daylight or office lighting preferred
   - Avoid backlighting

4. **Resolution**
   - Minimum: 480x360 pixels
   - Recommended: 1920x1440 pixels or higher

5. **File Format**
   - JPG (quality 85+)
   - PNG
   - BMP

6. **Background**
   - Plain white or light background preferred
   - Natural background (office, classroom) acceptable
   - Avoid busy patterns
   - Avoid other faces in background

7. **Face Features**
   - Eyes clearly visible and open
   - Natural facial expression (neutral or slight smile)
   - Hair not covering face
   - No sunglasses or excessive accessories
   - Beard/mustache acceptable (consistent across photos)

**Example: Recommended Photo Set**

For each student, capture:
- `photo1.jpg` - Front-facing, neutral expression
- `photo2.jpg` - Slight left tilt
- `photo3.jpg` - Slight right tilt
- `photo4.jpg` - Different lighting condition
- `photo5.jpg` - Different hairstyle or with glasses (if applicable)

---

## Dataset Setup Methods

### Method 1: Manual Directory Creation (Recommended for Small Groups)

Perfect for: 5-20 students

1. Create directories manually:
   ```bash
   mkdir dataset/known_faces/John_Doe_A001
   mkdir dataset/known_faces/Jane_Smith_A002
   mkdir dataset/known_faces/Bob_Johnson_A003
   ```

2. Copy photos into each directory:
   ```bash
   cp photos/john*.jpg dataset/known_faces/John_Doe_A001/
   cp photos/jane*.jpg dataset/known_faces/Jane_Smith_A002/
   ```

3. Register with batch import:
   ```bash
   python3 registration_utility.py --mode batch --dir dataset/known_faces
   ```

### Method 2: Bulk Directory Creation with Script

Perfect for: 50+ students

**Create `setup_dataset.sh` (Linux/macOS):**
```bash
#!/bin/bash

# Create directories from CSV file
# CSV format: FirstName,LastName,RollNumber

while IFS=',' read -r first last roll; do
    dir_name="${first}_${last}_${roll}"
    mkdir -p "dataset/known_faces/$dir_name"
    echo "Created: $dir_name"
done < students.csv
```

**Use it:**
```bash
chmod +x setup_dataset.sh
./setup_dataset.sh
```

**Create `setup_dataset.ps1` (Windows PowerShell):**
```powershell
# CSV format: FirstName,LastName,RollNumber
$students = Import-Csv -Path "students.csv"

foreach ($student in $students) {
    $dirName = "{0}_{1}_{2}" -f $student.FirstName, $student.LastName, $student.RollNumber
    New-Item -ItemType Directory -Path "dataset\known_faces\$dirName" -Force
    Write-Host "Created: $dirName"
}
```

**CSV Format (`students.csv`):**
```csv
FirstName,LastName,RollNumber
John,Doe,A001
Jane,Smith,A002
Bob,Johnson,A003
Alice,Williams,A004
Charlie,Brown,A005
```

### Method 3: Real-time Camera Capture

Perfect for: On-site registration

```bash
# Register one student while capturing photos
python3 registration_utility.py --mode capture --name "John Doe" --roll "A001"

# Then follow interactive prompts:
# - Press SPACE to capture photo
# - Press ESC to skip
# - Press Q when done
```

### Method 4: Single Photo Import

Perfect for: Existing photo library

```bash
# Register individual student
python3 registration_utility.py --mode single \
    --name "John Doe" \
    --roll "A001" \
    --image "photos/john_doe.jpg"
```

---

## CSV Import Format

**Create `students_with_photos.csv`:**

```csv
Name,RollNumber,PhotoPath
John Doe,A001,/path/to/john_doe.jpg
Jane Smith,A002,/path/to/jane_smith.jpg
Bob Johnson,A003,/path/to/bob_johnson.jpg
Alice Williams,A004,/path/to/alice_williams.jpg
```

**Python script to batch import:**

```python
import csv
from registration_utility import StudentRegistration

registration = StudentRegistration()

with open('students_with_photos.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']
        roll = row['RollNumber']
        photo = row['PhotoPath']
        
        print(f"Registering {name}...")
        registration.register_single_student(name, roll, photo)
        print(f"✓ {name} registered\n")
```

---

## Validating Your Dataset

### Check Directory Structure

```bash
# List all student directories
ls -la dataset/known_faces/

# Check files in a student directory
ls -la dataset/known_faces/John_Doe_A001/

# Count total photos
find dataset/known_faces -type f -name "*.jpg" | wc -l
```

### Verify Photo Quality

```python
import cv2
import os

dataset_dir = "dataset/known_faces"

for student_dir in os.listdir(dataset_dir):
    student_path = os.path.join(dataset_dir, student_dir)
    if os.path.isdir(student_path):
        print(f"\n{student_dir}:")
        
        for photo in os.listdir(student_path):
            photo_path = os.path.join(student_path, photo)
            
            img = cv2.imread(photo_path)
            if img is None:
                print(f"  ✗ {photo}: Cannot read")
                continue
            
            h, w = img.shape[:2]
            print(f"  ✓ {photo}: {w}x{h}")
            
            if h < 360 or w < 480:
                print(f"     WARNING: Low resolution")
```

### Test Face Detection

```python
from face_recognition import FaceRecognitionEngine
import os

engine = FaceRecognitionEngine()
dataset_dir = "dataset/known_faces"

for student_dir in os.listdir(dataset_dir):
    student_path = os.path.join(dataset_dir, student_dir)
    photo_path = os.path.join(student_path, os.listdir(student_path)[0])
    
    embedding = engine.generate_embedding_from_image(photo_path)
    
    if embedding is not None:
        print(f"✓ {student_dir}: Face detected")
    else:
        print(f"✗ {student_dir}: Face NOT detected - Check photo quality!")
```

---

## Common Dataset Issues & Solutions

### Issue 1: Duplicate Roll Numbers

**Problem:** Two students with same roll number

**Solution:**
```bash
# Rename directory to make unique
mv dataset/known_faces/John_Doe_A001 dataset/known_faces/John_Doe_A001_v2
```

### Issue 2: Invalid Directory Name (with spaces/hyphens)

**Problem:** Directory named `Alice Johnson - 2024`

**Solution:**
```bash
# Rename with correct format
mv "dataset/known_faces/Alice Johnson - 2024" dataset/known_faces/Alice_Johnson_2024
```

### Issue 3: Corrupted or Unreadable Photos

**Solution:**
```bash
# Remove corrupted file
rm dataset/known_faces/John_Doe_A001/corrupted.jpg

# Add replacement photo
cp replacement.jpg dataset/known_faces/John_Doe_A001/photo1.jpg
```

### Issue 4: Face Not Detected in Photos

**Problem:** Photos too small or faces not visible

**Solution:**
```bash
# Replace with better quality photos
# Ensure face occupies 30-70% of image
# Recapture with better lighting
python3 registration_utility.py --mode single \
    --name "John Doe" \
    --roll "A001" \
    --image "dataset/known_faces/John_Doe_A001/better_photo.jpg"
```

---

## Dataset Statistics

After setup, check your dataset:

```python
import os

dataset_dir = "dataset/known_faces"

total_students = len(os.listdir(dataset_dir))
total_photos = sum(len(files) for _, _, files in os.walk(dataset_dir))
photos_per_student = total_photos / total_students if total_students > 0 else 0

print(f"Total Students: {total_students}")
print(f"Total Photos: {total_photos}")
print(f"Avg Photos/Student: {photos_per_student:.1f}")

# List students with few photos
print("\nStudents with < 3 photos:")
for student_dir in os.listdir(dataset_dir):
    student_path = os.path.join(dataset_dir, student_dir)
    photo_count = len([f for f in os.listdir(student_path) if f.endswith(('.jpg', '.png'))])
    if photo_count < 3:
        print(f"  {student_dir}: {photo_count} photos")
```

---

## Performance Notes

- **More photos:** Better accuracy (3-5 optimal)
- **Better quality photos:** Fewer false positives
- **Diverse angles:** Better recognition in real-time
- **Storage:** ~100KB-500KB per student (depends on resolution)

---

## Next Steps

1. ✓ Create directory structure
2. ✓ Add student photos
3. ✓ Validate dataset
4. Run batch registration: `python3 registration_utility.py --mode batch --dir dataset/known_faces`
5. Start attendance: `python3 attendance_system.py --headless`

For detailed installation steps, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

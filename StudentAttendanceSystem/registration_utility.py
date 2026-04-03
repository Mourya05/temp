"""
Student Registration Utility
Batch register students or register individual students with face detection
"""

import os
import cv2
import argparse
from pathlib import Path
from attendance_system import AttendanceSystem


class StudentRegistration:
    """Utility for registering students"""
    
    def __init__(self):
        self.system = AttendanceSystem()
    
    def register_from_directory(self, dataset_dir):
        """
        Register all students from a directory structure:
        dataset/known_faces/
        ├── Student1_Roll001/
        │   ├── image1.jpg
        │   ├── image2.jpg
        └── Student2_Roll002/
            ├── image1.jpg
            └── image2.jpg
        """
        dataset_path = Path(dataset_dir)
        
        if not dataset_path.exists():
            print(f"[ERROR] Directory not found: {dataset_dir}")
            return
        
        student_dirs = [d for d in dataset_path.iterdir() if d.is_dir()]
        total_registered = 0
        
        print(f"\n[REGISTRATION] Processing {len(student_dirs)} student directories...")
        
        for student_dir in sorted(student_dirs):
            try:
                # Parse directory name: "StudentName_RollNumber"
                dir_name = student_dir.name
                parts = dir_name.rsplit('_', 1)
                
                if len(parts) != 2:
                    print(f"[SKIP] Invalid directory name format: {dir_name}")
                    print("       Expected format: StudentName_RollNumber")
                    continue
                
                name, roll_number = parts
                
                # Find image files
                image_files = list(student_dir.glob('*.jpg')) + list(student_dir.glob('*.png'))
                
                if not image_files:
                    print(f"[SKIP] No images found in {dir_name}")
                    continue
                
                # Use first image for registration
                image_path = str(image_files[0])
                
                print(f"\n[PROCESSING] {name} ({roll_number})")
                print(f"   Image: {image_files[0].name}")
                print(f"   Found {len(image_files)} image(s) in directory")
                
                success = self.system.register_student_from_image(name, roll_number, image_path)
                
                if success:
                    print(f"   ✓ Registration successful")
                    total_registered += 1
                else:
                    print(f"   ✗ Registration failed")
            
            except Exception as e:
                print(f"[ERROR] Failed to process {student_dir.name}: {e}")
        
        print(f"\n{'='*60}")
        print(f"Registration complete: {total_registered}/{len(student_dirs)} students registered")
        print(f"{'='*60}\n")
    
    def register_single_student(self, name, roll_number, image_path):
        """Register a single student"""
        print(f"\n[REGISTRATION] Registering: {name} ({roll_number})")
        
        if not os.path.exists(image_path):
            print(f"[ERROR] Image file not found: {image_path}")
            return False
        
        success = self.system.register_student_from_image(name, roll_number, image_path)
        
        if success:
            print("[SUCCESS] Student registered successfully")
        else:
            print("[FAILED] Student registration failed")
        
        return success
    
    def capture_student_photo(self, name, roll_number, num_photos=5):
        """
        Capture photos of a student using camera
        Returns the path of the best quality photo
        """
        print(f"\n[CAPTURE] Preparing to capture photos for {name} ({roll_number})")
        print(f"Press SPACE to capture, ESC to skip, Q to finish")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("[ERROR] Could not open camera")
            return None
        
        captured_photos = []
        photo_count = 0
        
        print(f"\nCapturing {num_photos} photos...")
        
        while photo_count < num_photos:
            ret, frame = cap.read()
            
            if not ret:
                print("[ERROR] Failed to read frame")
                break
            
            # Resize for display
            display_frame = cv2.resize(frame, (640, 480))
            cv2.putText(display_frame, f"Photo {photo_count + 1}/{num_photos}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, "SPACE=Capture  ESC=Skip  Q=Finish", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
            
            cv2.imshow('Capture Student Photo', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space key
                # Save photo
                photo_dir = Path("student_photos")
                photo_dir.mkdir(exist_ok=True)
                
                photo_path = photo_dir / f"{roll_number}_{photo_count}.jpg"
                cv2.imwrite(str(photo_path), frame)
                
                captured_photos.append(str(photo_path))
                photo_count += 1
                print(f"[CAMERA] Captured photo {photo_count}")
            
            elif key == 27:  # ESC key
                continue
            
            elif key == ord('q'):  # Q key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if captured_photos:
            best_photo = captured_photos[0]  # Use first photo as best
            print(f"\n[CAPTURE] Using photo: {best_photo}")
            return best_photo
        else:
            print("[CAPTURE] No photos captured")
            return None


def main():
    """Command-line registration utility"""
    
    parser = argparse.ArgumentParser(
        description='Student Registration Utility for Attendance System'
    )
    
    parser.add_argument(
        '--mode', 
        choices=['batch', 'single', 'capture'],
        default='batch',
        help='Registration mode (default: batch)'
    )
    
    parser.add_argument(
        '--dir',
        help='Directory path for batch registration'
    )
    
    parser.add_argument(
        '--name',
        help='Student name for single registration'
    )
    
    parser.add_argument(
        '--roll',
        help='Student roll number'
    )
    
    parser.add_argument(
        '--image',
        help='Image path for single registration'
    )
    
    args = parser.parse_args()
    
    registration = StudentRegistration()
    
    if args.mode == 'batch':
        if not args.dir:
            print("[ERROR] --dir is required for batch mode")
            return
        registration.register_from_directory(args.dir)
    
    elif args.mode == 'single':
        if not all([args.name, args.roll, args.image]):
            print("[ERROR] --name, --roll, and --image are required for single mode")
            return
        registration.register_single_student(args.name, args.roll, args.image)
    
    elif args.mode == 'capture':
        if not all([args.name, args.roll]):
            print("[ERROR] --name and --roll are required for capture mode")
            return
        photo_path = registration.capture_student_photo(args.name, args.roll)
        if photo_path:
            registration.register_single_student(args.name, args.roll, photo_path)


if __name__ == "__main__":
    main()

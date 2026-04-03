"""
Face Recognition Engine for Student Attendance System
Uses Mediapipe for ARM-optimized face detection and recognition
"""

import cv2
import mediapipe as mp
import numpy as np
import os
from pathlib import Path
import pickle


class FaceRecognitionEngine:
    """Face detection and recognition using Mediapipe"""
    
    def __init__(self, model_confidence=0.5):
        """Initialize Mediapipe face detection"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 1 for better accuracy on close-up faces
            min_detection_confidence=model_confidence
        )
        
        # For face recognition, we'll use face embeddings (simple approach)
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        
        print("[FACE_ENGINE] Mediapipe FaceDetection initialized")
    
    def extract_face_embedding(self, frame, detection):
        """
        Extract face region and create a simple embedding
        For production, consider using mediapipe face mesh for detailed features
        """
        h, w, c = frame.shape
        
        # Get bounding box from detection
        bbox = detection.location_data.bounding_box
        x_min = int(bbox.xmin * w)
        y_min = int(bbox.ymin * h)
        x_max = int((bbox.xmin + bbox.width) * w)
        y_max = int((bbox.ymin + bbox.height) * h)
        
        # Ensure coordinates are within bounds
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w, x_max)
        y_max = min(h, y_max)
        
        # Extract face region
        face_region = frame[y_min:y_max, x_min:x_max]
        
        if face_region.size == 0:
            return None, (x_min, y_min, x_max, y_max)
        
        # Create a simple embedding by resizing and flattening
        # For production, use more sophisticated methods like OpenFace or FaceNet
        face_resized = cv2.resize(face_region, (128, 128))
        face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
        embedding = face_gray.flatten().astype(np.float32)
        
        return embedding, (x_min, y_min, x_max, y_max)
    
    def detect_faces(self, frame):
        """Detect faces in a frame using Mediapipe"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame_rgb)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                embedding, bbox = self.extract_face_embedding(frame, detection)
                if embedding is not None:
                    confidence = detection.location_data.relative_keypoints[0].z if hasattr(detection.location_data, 'relative_keypoints') else 0.9
                    faces.append({
                        'embedding': embedding,
                        'bbox': bbox,
                        'confidence': confidence
                    })
        
        return faces
    
    def calculate_face_distance(self, face_encoding1, face_encoding2):
        """Calculate Euclidean distance between two face encodings"""
        if face_encoding1 is None or face_encoding2 is None:
            return float('inf')
        
        return np.linalg.norm(face_encoding1 - face_encoding2)
    
    def compare_faces(self, face_encodings, face_to_compare, tolerance=50.0):
        """Compare a face to a list of known faces"""
        distances = []
        for encoding in face_encodings:
            distance = self.calculate_face_distance(encoding, face_to_compare)
            distances.append(distance)
        
        return distances
    
    def recognize_face(self, face_embedding, tolerance=40.0):
        """
        Recognize a face by comparing to known faces
        Returns (student_id, name, confidence) or (None, "Unknown", 0)
        """
        if len(self.known_face_encodings) == 0:
            return None, "Unknown", 0
        
        distances = self.compare_faces(self.known_face_encodings, face_embedding, tolerance)
        min_distance = min(distances)
        
        if min_distance < tolerance:
            min_index = distances.index(min_distance)
            confidence = max(0, 1 - (min_distance / tolerance))
            return (self.known_face_ids[min_index], 
                    self.known_face_names[min_index], 
                    confidence)
        
        return None, "Unknown", 0
    
    def load_known_faces_from_db(self, students):
        """Load known face encodings from database"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        
        for student in students:
            student_id, name, roll_number, face_encoding = student
            try:
                # Deserialize face encoding from database
                encoding = pickle.loads(face_encoding)
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)
                self.known_face_ids.append(student_id)
            except Exception as e:
                print(f"[WARNING] Failed to load encoding for {name}: {e}")
        
        print(f"[FACE_ENGINE] Loaded {len(self.known_face_encodings)} face encodings")
    
    def generate_embedding_from_image(self, image_path):
        """Generate face embedding from an image file"""
        try:
            frame = cv2.imread(image_path)
            if frame is None:
                print(f"[ERROR] Failed to load image: {image_path}")
                return None
            
            # Resize for faster processing
            h, w = frame.shape[:2]
            if h > 480 or w > 640:
                scale = min(480/h, 640/w)
                frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
            
            faces = self.detect_faces(frame)
            
            if len(faces) > 0:
                # Use the first (and usually only) face detected
                return faces[0]['embedding']
            else:
                print(f"[WARNING] No face detected in {image_path}")
                return None
        except Exception as e:
            print(f"[ERROR] Failed to generate embedding: {e}")
            return None
    
    def draw_face_boxes(self, frame, faces, labels):
        """Draw bounding boxes around detected faces"""
        for face_data, label in zip(faces, labels):
            bbox = face_data['bbox']
            x_min, y_min, x_max, y_max = bbox
            
            # Choose color based on label
            if label == "Unknown":
                color = (0, 0, 255)  # Red for unknown
            else:
                color = (0, 255, 0)  # Green for known
            
            # Draw rectangle
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
            
            # Put label
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, 
                         (x_min, y_min - text_size[1] - 4), 
                         (x_min + text_size[0], y_min), 
                         color, -1)
            cv2.putText(frame, label, 
                       (x_min, y_min - 2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def cleanup(self):
        """Clean up resources"""
        self.face_detection.close()
        print("[FACE_ENGINE] Cleaned up resources")

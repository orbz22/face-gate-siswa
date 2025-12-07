"""
Face Recognition - LBPH + Haarcascade dengan Save/Load Model
"""
import cv2
import numpy as np
import os
import json
import config


class FaceRecognition:
    def __init__(self):
        self.face_cascade = None
        self.recognizer = None
        self.is_trained = False
        self.label_to_user = {}
        
        self._ensure_directories()
        self._load_cascade()
        self._init_recognizer()
        self._load_model()  # Auto load model saat startup
    
    def _ensure_directories(self):
        """Buat folder yang diperlukan"""
        os.makedirs(config.MODEL_DIR, exist_ok=True)
    
    def _load_cascade(self):
        """Load Haarcascade"""
        try:
            if os.path.exists(config.HAARCASCADE_FILE):
                self.face_cascade = cv2.CascadeClassifier(config.HAARCASCADE_FILE)
            else:
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                print("❌ Failed to load Haarcascade")
                self.face_cascade = None
            else:
                print("✅ Haarcascade loaded")
                
        except Exception as e:
            print(f"❌ Error loading cascade: {e}")
            self.face_cascade = None
    
    def _init_recognizer(self):
        """Initialize LBPH Recognizer"""
        try:
            if not hasattr(cv2, 'face'):
                print("❌ cv2.face module not found!")
                self.recognizer = None
                return
            
            if not hasattr(cv2.face, 'LBPHFaceRecognizer_create'):
                print("❌ LBPHFaceRecognizer_create not found!")
                self.recognizer = None
                return
            
            self.recognizer = cv2.face.LBPHFaceRecognizer_create(
                radius=config.LBPH_RADIUS,
                neighbors=config.LBPH_NEIGHBORS,
                grid_x=config.LBPH_GRID_X,
                grid_y=config.LBPH_GRID_Y
            )
            print("✅ LBPH Recognizer initialized")
            
        except Exception as e:
            print(f"❌ Error initializing recognizer: {e}")
            self.recognizer = None
    
    def is_ready(self):
        """Check if face recognition is ready"""
        return self.face_cascade is not None and self.recognizer is not None
    
    def _load_model(self):
        """Load trained model dari file"""
        try:
            if not os.path.exists(config.MODEL_FILE):
                print("ℹ️ No saved model found")
                return False
            
            if not os.path.exists(config.LABELS_FILE):
                print("ℹ️ No saved labels found")
                return False
            
            if self.recognizer is None:
                print("❌ Recognizer not initialized")
                return False
            
            # Load model
            self.recognizer.read(config.MODEL_FILE)
            
            # Load labels
            with open(config.LABELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert string keys back to int
                self.label_to_user = {int(k): v for k, v in data.items()}
            
            self.is_trained = True
            print(f"✅ Model loaded: {len(self.label_to_user)} users")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def _save_model(self):
        """Save trained model ke file"""
        try:
            if self.recognizer is None:
                print("❌ Recognizer not initialized")
                return False
            
            if not self.is_trained:
                print("❌ Model not trained yet")
                return False
            
            # Save model
            self.recognizer.write(config.MODEL_FILE)
            
            # Save labels
            with open(config.LABELS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.label_to_user, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Model saved: {config.MODEL_FILE}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving model: {e}")
            return False
    
    def detect_faces(self, frame):
        """Detect faces in frame"""
        if self.face_cascade is None:
            return []
        
        try:
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            else:
                gray = frame
            
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=config.FACE_SCALE_FACTOR,
                minNeighbors=config.FACE_MIN_NEIGHBORS,
                minSize=config.FACE_MIN_SIZE
            )
            
            return faces
            
        except Exception as e:
            return []
    
    def extract_face(self, frame, face_rect):
        """Extract face region from frame"""
        x, y, w, h = face_rect
        
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        else:
            gray = frame
        
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        
        return face
    
    def save_face(self, frame, face_rect, user_id, face_dir):
        """Save face image for training"""
        try:
            face = self.extract_face(frame, face_rect)
            
            existing_faces = len([f for f in os.listdir(face_dir) if f.endswith('.jpg')])
            
            filename = os.path.join(face_dir, f"face_{existing_faces + 1}.jpg")
            cv2.imwrite(filename, face)
            
            print(f"✅ Face saved: {filename}")
            return existing_faces + 1
            
        except Exception as e:
            print(f"❌ Error saving face: {e}")
            return -1
    
    def train(self, users):
        """Train recognizer dengan semua user faces"""
        if self.recognizer is None:
            print("❌ Recognizer not initialized!")
            return False
        
        if not users:
            print("⚠️ No users to train")
            return False
        
        try:
            faces = []
            labels = []
            self.label_to_user = {}
            
            for user in users:
                user_id = user["id"]
                face_dir = user["face_dir"]
                
                if not os.path.exists(face_dir):
                    continue
                
                for filename in os.listdir(face_dir):
                    if filename.endswith('.jpg'):
                        filepath = os.path.join(face_dir, filename)
                        face = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                        
                        if face is not None:
                            face = cv2.resize(face, (200, 200))
                            faces.append(face)
                            labels.append(user_id)
                            self.label_to_user[user_id] = user
            
            if not faces:
                print("⚠️ No face images found")
                return False
            
            # Train
            self.recognizer.train(faces, np.array(labels))
            self.is_trained = True
            
            # Save model ke file
            self._save_model()
            
            print(f"✅ Trained with {len(faces)} faces from {len(self.label_to_user)} users")
            return True
            
        except Exception as e:
            print(f"❌ Error training: {e}")
            return False
    
    def recognize(self, frame, face_rect):
        """Recognize face"""
        if self.recognizer is None:
            return None, 0
        
        if not self.is_trained:
            return None, 0
        
        try:
            face = self.extract_face(frame, face_rect)
            
            label, confidence = self.recognizer.predict(face)
            
            if confidence < config.CONFIDENCE_THRESHOLD:
                user = self.label_to_user.get(label)
                return user, confidence
            else:
                return None, confidence
                
        except Exception as e:
            return None, 0
    
    def draw_faces(self, frame, faces, recognized_users=None):
        """Draw rectangles around faces"""
        frame_copy = frame.copy()
        
        for i, (x, y, w, h) in enumerate(faces):
            if recognized_users and i < len(recognized_users):
                user, confidence = recognized_users[i]
                if user:
                    color = (0, 255, 0)
                    label = f"{user['nama_anak']} ({100-confidence:.0f}%)"
                else:
                    color = (255, 0, 0)
                    label = "Unknown"
            else:
                color = (255, 255, 0)
                label = "Detecting..."
            
            cv2.rectangle(frame_copy, (x, y), (x+w, y+h), color, 2)
            
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            cv2.rectangle(frame_copy, (x, y - 25), (x + label_size[0] + 10, y), color, -1)
            
            cv2.putText(frame_copy, label, (x + 5, y - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        return frame_copy
    
    def delete_model(self):
        """Hapus model file"""
        try:
            if os.path.exists(config.MODEL_FILE):
                os.remove(config.MODEL_FILE)
            if os.path.exists(config.LABELS_FILE):
                os.remove(config.LABELS_FILE)
            
            self.is_trained = False
            self.label_to_user = {}
            
            print("✅ Model deleted")
            return True
        except Exception as e:
            print(f"❌ Error deleting model: {e}")
            return False
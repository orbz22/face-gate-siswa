"""
Camera Handler
"""
import cv2
import threading
import time
import os
import sys

# Suppress ALL OpenCV warnings
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"

# Redirect stderr temporarily for OpenCV
class SuppressStream:
    def __init__(self):
        self.null = open(os.devnull, 'w')
        self.old_stderr = None
    
    def __enter__(self):
        self.old_stderr = sys.stderr
        sys.stderr = self.null
        return self
    
    def __exit__(self, *args):
        sys.stderr = self.old_stderr
        self.null.close()


class CameraHandler:
    # Cache available cameras
    _cached_cameras = None
    
    def __init__(self, camera_index=0, width=1920, height=1080):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        
        self.cap = None
        self.frame = None
        self.is_running = False
        self.thread = None
        self.lock = threading.Lock()
        
        # Flip settings
        self.flip_horizontal = False
        self.flip_vertical = False
    
    def start(self):
        """Start camera"""
        if self.is_running:
            return True
        
        try:
            with SuppressStream():
                # Use DSHOW on Windows
                if os.name == 'nt':
                    self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
                else:
                    self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                print(f"❌ Failed to open camera {self.camera_index}")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"✅ Camera {self.camera_index} started: {actual_w}x{actual_h}")
            
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Camera error: {e}")
            return False
    
    def _capture_loop(self):
        """Capture loop"""
        while self.is_running:
            try:
                if self.cap and self.cap.isOpened():
                    ret, frame = self.cap.read()
                    
                    if ret and frame is not None:
                        # Apply flip
                        if self.flip_horizontal and self.flip_vertical:
                            frame = cv2.flip(frame, -1)
                        elif self.flip_horizontal:
                            frame = cv2.flip(frame, 1)
                        elif self.flip_vertical:
                            frame = cv2.flip(frame, 0)
                        
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        with self.lock:
                            self.frame = frame_rgb
                
                time.sleep(0.01)
                
            except:
                time.sleep(0.1)
    
    def get_frame(self):
        """Get current frame"""
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
        return None
    
    def stop(self):
        """Stop camera"""
        self.is_running = False
        
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None
        
        if self.cap:
            with SuppressStream():
                self.cap.release()
            self.cap = None
        
        print(f"✅ Camera {self.camera_index} stopped")
    
    def change_camera(self, new_index):
        """Change camera"""
        if new_index == self.camera_index:
            return True
            
        print(f"🔄 Changing camera to {new_index}...")
        was_running = self.is_running
        
        if was_running:
            self.stop()
            time.sleep(0.3)
        
        self.camera_index = new_index
        
        if was_running:
            return self.start()
        return True
    
    def get_available_cameras(self, max_check=3):
        """Get available cameras (cached, no warnings)"""
        # Return cached if available
        if CameraHandler._cached_cameras is not None:
            return CameraHandler._cached_cameras
        
        available = []
        
        # Current camera is always available
        available.append(self.camera_index)
        
        # Check others with suppressed output
        with SuppressStream():
            for i in range(max_check):
                if i == self.camera_index:
                    continue
                try:
                    if os.name == 'nt':
                        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                    else:
                        cap = cv2.VideoCapture(i)
                    
                    if cap.isOpened():
                        ret, _ = cap.read()
                        if ret:
                            available.append(i)
                        cap.release()
                except:
                    pass
        
        # Sort and cache
        available = sorted(list(set(available)))
        CameraHandler._cached_cameras = available
        
        return available
    
    @staticmethod
    def clear_camera_cache():
        """Clear camera cache"""
        CameraHandler._cached_cameras = None
    
    def __del__(self):
        self.stop()
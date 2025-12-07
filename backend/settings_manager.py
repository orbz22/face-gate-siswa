"""
Settings Manager
"""
import json
import os

class SettingsManager:
    DEFAULT = {
        "camera_index": 0,
        "flip_horizontal": False,
        "flip_vertical": False,
        "fullscreen": False,
        "show_fps": False
    }
    
    def __init__(self, filepath="data/settings.json"):
        self.filepath = filepath
        self.settings = {}
        self._load()
    
    def _load(self):
        """Load settings"""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            
            if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
                with open(self.filepath, 'r') as f:
                    self.settings = json.load(f)
                print(f"✅ Settings loaded")
            else:
                self.settings = self.DEFAULT.copy()
                self._save()
                print(f"📝 Default settings created")
        except:
            self.settings = self.DEFAULT.copy()
    
    def _save(self):
        """Save settings"""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    # Getters
    def get_camera_index(self):
        return self.settings.get("camera_index", 0)
    
    def get_camera_flip_horizontal(self):
        return self.settings.get("flip_horizontal", False)
    
    def get_camera_flip_vertical(self):
        return self.settings.get("flip_vertical", False)
    
    def get_fullscreen(self):
        return self.settings.get("fullscreen", False)
    
    def get_show_fps(self):
        return self.settings.get("show_fps", False)
    
    # Setters
    def set_camera_index(self, val):
        self.settings["camera_index"] = val
        self._save()
    
    def set_camera_flip_horizontal(self, val):
        self.settings["flip_horizontal"] = val
        self._save()
    
    def set_camera_flip_vertical(self, val):
        self.settings["flip_vertical"] = val
        self._save()
    
    def set_fullscreen(self, val):
        self.settings["fullscreen"] = val
        self._save()
    
    def set_show_fps(self, val):
        self.settings["show_fps"] = val
        self._save()
    
    def reset_to_default(self):
        self.settings = self.DEFAULT.copy()
        self._save()
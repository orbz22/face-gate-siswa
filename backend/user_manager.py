"""
User Manager - Mengelola data pengguna
"""
import json
import os
from datetime import datetime
import config


class UserManager:
    def __init__(self):
        self.users = []
        self._ensure_directories()
        self._load()
    
    def _ensure_directories(self):
        """Buat folder yang diperlukan"""
        os.makedirs(config.DATA_DIR, exist_ok=True)
        os.makedirs(config.FACES_DIR, exist_ok=True)
    
    def _load(self):
        """Load data users"""
        try:
            if os.path.exists(config.USERS_FILE):
                with open(config.USERS_FILE, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
                print(f"✅ Loaded {len(self.users)} users")
            else:
                self.users = []
                self._save()
        except Exception as e:
            print(f"❌ Error loading users: {e}")
            self.users = []
    
    def _save(self):
        """Save data users"""
        try:
            with open(config.USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving users: {e}")
            return False
    
    def add_user(self, nama_ortu, nama_anak, kelas):
        """Tambah user baru"""
        user_id = len(self.users) + 1
        
        # Buat folder untuk wajah user
        user_face_dir = os.path.join(config.FACES_DIR, f"user_{user_id}")
        os.makedirs(user_face_dir, exist_ok=True)
        
        user = {
            "id": user_id,
            "nama_ortu": nama_ortu,
            "nama_anak": nama_anak,
            "kelas": kelas,
            "face_dir": user_face_dir,
            "face_count": 0,
            "registered_at": datetime.now().isoformat(),
            "last_seen": None
        }
        
        self.users.append(user)
        self._save()
        
        print(f"✅ User added: {nama_anak} (ID: {user_id})")
        return user
    
    def get_user(self, user_id):
        """Get user by ID"""
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None
    
    def get_user_by_name(self, nama_anak):
        """Get user by nama anak"""
        for user in self.users:
            if user["nama_anak"].lower() == nama_anak.lower():
                return user
        return None
    
    def get_all_users(self):
        """Get semua users"""
        return self.users.copy()
    
    def update_face_count(self, user_id, count):
        """Update jumlah foto wajah"""
        for user in self.users:
            if user["id"] == user_id:
                user["face_count"] = count
                self._save()
                return True
        return False
    
    def update_last_seen(self, user_id):
        """Update waktu terakhir terlihat"""
        for user in self.users:
            if user["id"] == user_id:
                user["last_seen"] = datetime.now().isoformat()
                self._save()
                return True
        return False
    
    def delete_user(self, user_id):
        """Hapus user"""
        import shutil
        
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                # Hapus folder wajah
                if os.path.exists(user["face_dir"]):
                    shutil.rmtree(user["face_dir"])
                
                # Hapus dari list
                self.users.pop(i)
                self._save()
                print(f"✅ User deleted: ID {user_id}")
                return True
        return False
    
    def get_user_count(self):
        """Get jumlah user"""
        return len(self.users)
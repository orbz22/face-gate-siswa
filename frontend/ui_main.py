"""
Main UI - dengan Button Panel dan Face Recognition
"""
import tkinter as tk
from .components import CameraFrame, ButtonPanel
from .pages import SettingsPage, RegisterPage
from backend import CameraHandler, SettingsManager, UserManager, FaceRecognition
import config


class MainUI:
    def __init__(self, root):
        self.root = root
        self.current_page = None
        self.camera_frame = None
        self.button_panel = None
        self.is_main_page = False
        self.scan_active = False
        
        # Setup window
        self._setup_window()
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.user_manager = UserManager()
        self.face_recognition = FaceRecognition()
        
        # Initialize camera
        self.camera_handler = CameraHandler(
            camera_index=self.settings_manager.get_camera_index(),
            width=config.CAMERA_WIDTH,
            height=config.CAMERA_HEIGHT
        )
        self.camera_handler.flip_horizontal = self.settings_manager.get_camera_flip_horizontal()
        self.camera_handler.flip_vertical = self.settings_manager.get_camera_flip_vertical()
        
        # Start camera
        self.camera_handler.start()
        
        # Train face recognition if users exist
        self._train_recognizer()
        
        # Show main page
        self._show_main_page()
        
        # Start update loop
        self._update_loop()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<Escape>", lambda e: self._on_close())
        self.root.bind("<f>", lambda e: self._toggle_fullscreen())
        self.root.bind("<F>", lambda e: self._toggle_fullscreen())
        
        self.is_fullscreen = self.settings_manager.get_fullscreen()
        if self.is_fullscreen:
            self.root.attributes('-fullscreen', True)
    
    def _setup_window(self):
        """Setup window"""
        self.root.title(config.APP_NAME)
        self.root.geometry(f"{config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=config.COLOR_BLACK)
        
        # Center
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - config.SCREEN_WIDTH) // 2
        y = (self.root.winfo_screenheight() - config.SCREEN_HEIGHT) // 2
        self.root.geometry(f"+{x}+{y}")
    
    def _train_recognizer(self):
        """Train face recognizer"""
        users = self.user_manager.get_all_users()
        if users:
            self.face_recognition.train(users)
    
    def _show_main_page(self):
        """Show main page"""
        print("📷 Showing main page...")
        
        if self.current_page:
            self.current_page.destroy()
        
        self.is_main_page = True
        
        # Main container
        self.current_page = tk.Frame(self.root, bg=config.COLOR_BLACK)
        self.current_page.pack(fill=tk.BOTH, expand=True)
        
        # Camera frame
        self.camera_frame = CameraFrame(
            self.current_page,
            on_settings_click=self._show_settings_page
        )
        self.camera_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button panel
        callbacks = {
            'scan': self._on_scan_toggle,
            'register': self._show_register_page,
            'info': self._show_info
        }
        self.button_panel = ButtonPanel(self.current_page, callbacks)
        self.button_panel.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Restore scan state
        self.button_panel.set_scan_state(self.scan_active)
        
        print("✅ Main page ready")
    
    def _show_settings_page(self):
        """Show settings page"""
        print("⚙️ Showing settings page...")
        
        self.is_main_page = False
        self.camera_frame = None
        
        if self.current_page:
            self.current_page.destroy()
        
        self.current_page = SettingsPage(
            self.root,
            on_back=self._show_main_page,
            camera_handler=self.camera_handler,
            settings_manager=self.settings_manager
        )
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def _show_register_page(self):
        """Show register page"""
        print("📝 Showing register page...")
        
        self.is_main_page = False
        self.camera_frame = None
        
        if self.current_page:
            self.current_page.destroy()
        
        self.current_page = RegisterPage(
            self.root,
            on_back=self._on_register_back,
            camera_handler=self.camera_handler,
            user_manager=self.user_manager,
            face_recognition=self.face_recognition
        )
        self.current_page.pack(fill=tk.BOTH, expand=True)
    
    def _on_register_back(self):
        """Callback when back from register"""
        # Retrain recognizer
        self._train_recognizer()
        self._show_main_page()
    
    def _show_info(self):
        """Show info/history"""
        from tkinter import messagebox
        
        users = self.user_manager.get_all_users()
        
        if not users:
            messagebox.showinfo("Info", "Belum ada user terdaftar.")
            return
        
        info = "📋 Daftar User Terdaftar:\n\n"
        for user in users:
            info += f"• {user['nama_anak']} ({user['kelas']})\n"
            info += f"  Ortu: {user['nama_ortu']}\n"
            info += f"  Foto: {user['face_count']} wajah\n\n"
        
        messagebox.showinfo("Daftar User", info)
    
    def _on_scan_toggle(self, active):
        """Handle scan toggle"""
        self.scan_active = active
        print(f"🔍 Scan: {'ON' if active else 'OFF'}")
    
    def _update_loop(self):
        """Update camera display"""
        try:
            if self.is_main_page and self.camera_frame:
                frame = self.camera_handler.get_frame()
                
                if frame is not None:
                    # If scanning, detect and recognize faces
                    if self.scan_active:
                        faces = self.face_recognition.detect_faces(frame)
                        
                        if len(faces) > 0:
                            recognized = []
                            for face in faces:
                                user, conf = self.face_recognition.recognize(frame, face)
                                recognized.append((user, conf))
                                
                                # Update last seen
                                if user:
                                    self.user_manager.update_last_seen(user["id"])
                            
                            frame = self.face_recognition.draw_faces(frame, faces, recognized)
                    
                    self.camera_frame.update_frame(frame)
                    
        except tk.TclError:
            pass
        except Exception as e:
            pass
        
        self.root.after(33, self._update_loop)
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        self.settings_manager.set_fullscreen(self.is_fullscreen)
        print(f"🖥️ Fullscreen: {'ON' if self.is_fullscreen else 'OFF'}")
    
    def _on_close(self):
        """Close app"""
        print("👋 Closing...")
        self.camera_handler.stop()
        self.root.destroy()
"""
Main UI
"""
import tkinter as tk
from .components import CameraFrame
from .pages import SettingsPage
from backend import CameraHandler, SettingsManager
import config

class MainUI:
    def __init__(self, root):
        self.root = root
        self.current_page = None
        self.camera_frame = None
        self.is_main_page = False
        
        # Setup window
        self._setup_window()
        
        # Settings manager
        self.settings_manager = SettingsManager()
        
        # Camera handler
        self.camera_handler = CameraHandler(
            camera_index=self.settings_manager.get_camera_index(),
            width=config.CAMERA_WIDTH,
            height=config.CAMERA_HEIGHT
        )
        self.camera_handler.flip_horizontal = self.settings_manager.get_camera_flip_horizontal()
        self.camera_handler.flip_vertical = self.settings_manager.get_camera_flip_vertical()
        
        # Start camera FIRST
        self.camera_handler.start()
        
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
    
    def _show_main_page(self):
        """Show main camera page"""
        print("📷 Showing main page...")
        
        # Destroy current page
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None
        
        # Set flag BEFORE creating frame
        self.is_main_page = True
        
        # Create camera frame
        self.camera_frame = CameraFrame(
            self.root,
            on_settings_click=self._show_settings_page
        )
        self.camera_frame.pack(fill=tk.BOTH, expand=True)
        
        self.current_page = self.camera_frame
        
        print("✅ Main page ready")
    
    def _show_settings_page(self):
        """Show settings page"""
        print("⚙️ Showing settings page...")
        
        # Set flag BEFORE destroying
        self.is_main_page = False
        self.camera_frame = None
        
        # Destroy current page
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None
        
        # Create settings page
        settings_page = SettingsPage(
            self.root,
            on_back=self._show_main_page,
            camera_handler=self.camera_handler,
            settings_manager=self.settings_manager
        )
        settings_page.pack(fill=tk.BOTH, expand=True)
        
        self.current_page = settings_page
        
        print("✅ Settings page ready")
    
    def _update_loop(self):
        """Update camera display"""
        try:
            # Only update if on main page AND camera_frame exists
            if self.is_main_page and self.camera_frame is not None:
                # Check if widget still exists
                if self.camera_frame.winfo_exists():
                    frame = self.camera_handler.get_frame()
                    
                    if frame is not None:
                        self.camera_frame.update_frame(frame)
                    
        except tk.TclError:
            # Widget was destroyed, ignore
            pass
        except Exception as e:
            pass
        
        # Always schedule next update
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
        self.is_main_page = False
        self.camera_handler.stop()
        self.root.destroy()
"""
Face Gate Siswa - Main Entry Point
"""
import tkinter as tk
from frontend import MainUI
import config

def main():
    print("=" * 50)
    print(f"🚀 {config.APP_NAME} v{config.APP_VERSION}")
    print(f"📺 Window: {config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
    print(f"📷 Camera: {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")
    print("=" * 50)
    print("Press ESC to exit | Press F for fullscreen")
    print("=" * 50)
    
    root = tk.Tk()
    app = MainUI(root)
    root.mainloop()
    
    print("✅ Application closed")

if __name__ == "__main__":
    main()
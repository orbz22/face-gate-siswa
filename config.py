"""
Konfigurasi Aplikasi Face Gate Siswa
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")

# Icon paths
ICON_SETTINGS = os.path.join(ICONS_DIR, "settings_icon.png")

# Window Settings
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# Camera Settings
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_INDEX = 0

# Colors
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_PRIMARY = "#2C3E50"
COLOR_SECONDARY = "#3498DB"
COLOR_SUCCESS = "#27AE60"
COLOR_WARNING = "#F39C12"
COLOR_DANGER = "#E74C3C"
COLOR_HOVER = "#5DADE2"
COLOR_SURFACE = "#ECF0F1"

# Font
FONT_FAMILY = "Helvetica"

# App Info
APP_NAME = "Face Gate Siswa"
APP_VERSION = "1.0.0"
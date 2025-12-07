"""
Konfigurasi Aplikasi Face Gate Siswa
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
HAARCASCADE_DIR = os.path.join(ASSETS_DIR, "haarcascade")

# Data
DATA_DIR = os.path.join(BASE_DIR, "data")
FACES_DIR = os.path.join(DATA_DIR, "faces")
MODEL_DIR = os.path.join(DATA_DIR, "model")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
MODEL_FILE = os.path.join(MODEL_DIR, "face_model.yml")
LABELS_FILE = os.path.join(MODEL_DIR, "labels.json")

# Icon paths
ICON_SETTINGS = os.path.join(ICONS_DIR, "settings_icon.png")

# Haarcascade
HAARCASCADE_FILE = os.path.join(HAARCASCADE_DIR, "haarcascade_frontalface_default.xml")

# Window Settings
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320

# Camera Settings
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_INDEX = 0

# Face Recognition Settings
FACE_MIN_SIZE = (100, 100)
FACE_SCALE_FACTOR = 1.2
FACE_MIN_NEIGHBORS = 5
LBPH_RADIUS = 1
LBPH_NEIGHBORS = 8
LBPH_GRID_X = 8
LBPH_GRID_Y = 8
CONFIDENCE_THRESHOLD = 70

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
COLOR_DARK = "#1A1A2E"

# Font
FONT_FAMILY = "Helvetica"

# App Info
APP_NAME = "Face Gate Siswa"
APP_VERSION = "1.0.0"
"""
Configuration file for Face Recognition Attendance System
"""

# Face Detection Settings
FACE_DETECTION_SCALE_FACTOR = 1.3
FACE_DETECTION_MIN_NEIGHBORS = 5

# Face Recognition Settings
KNN_NEIGHBORS = 5
FACE_IMAGE_SIZE = (50, 50)
IMAGES_PER_PERSON = 100

# File Paths
DATA_DIR = "data/"
ATTENDANCE_DIR = "Attendance/"
HAAR_CASCADE_PATH = "data/haarcascade_frontalface_default.xml"
FACES_DATA_PATH = "data/faces_data.pkl"
FACES_PATH = "data/faces.pkl"
NAMES_PATH = "data/names.pkl"

# Web Application Settings
FLASK_SECRET_KEY = "your_secret_key_here"  # Change this in production
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Attendance Settings
ATTENDANCE_DATE_FORMAT = "%d-%m-%Y"
ATTENDANCE_TIME_FORMAT = "%H:%M-%S"

# Video Capture Settings
CAMERA_INDEX = 0  # Default webcam
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# UI Settings
AUTO_REFRESH_INTERVAL = 2000  # milliseconds
AUTO_REFRESH_LIMIT = 100

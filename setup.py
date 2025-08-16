#!/usr/bin/env python3
"""
Setup script for Face Recognition Attendance System
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def create_directories():
    """Create necessary directories if they don't exist"""
    print("📁 Creating directories...")
    directories = ["data", "Attendance"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def check_haar_cascade():
    """Check if Haar Cascade file exists"""
    cascade_path = "data/haarcascade_frontalface_default.xml"
    if os.path.exists(cascade_path):
        print("✅ Haar Cascade file found")
        return True
    else:
        print("❌ Haar Cascade file not found")
        print("Please download haarcascade_frontalface_default.xml and place it in the data/ directory")
        return False

def create_sample_files():
    """Create sample configuration files"""
    print("📝 Creating sample files...")
    
    # Create sample attendance file
    sample_attendance = "Attendance/sample_attendance.csv"
    if not os.path.exists(sample_attendance):
        with open(sample_attendance, "w") as f:
            f.write("NAME,TIME\n")
            f.write("John Doe,09:00-15\n")
            f.write("Jane Smith,09:05-32\n")
        print("✅ Created sample attendance file")
    
    # Create sample names file
    sample_names = "data/sample_names.txt"
    if not os.path.exists(sample_names):
        with open(sample_names, "w") as f:
            f.write("# Sample Names File\n")
            f.write("# This file shows the expected format for names.pkl\n")
        print("✅ Created sample names file")

def main():
    """Main setup function"""
    print("🚀 Setting up Face Recognition Attendance System")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Check Haar Cascade
    if not check_haar_cascade():
        print("⚠️  Setup completed with warnings")
        print("Please download the Haar Cascade file to use face detection")
    else:
        print("✅ Setup completed successfully!")
    
    # Create sample files
    create_sample_files()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run 'python add_faces.py' to add new faces to the system")
    print("2. Run 'python test.py' to start face recognition")
    print("3. Run 'python web_app.py' to start the web interface")
    print("4. Run 'streamlit run app.py' to start the Streamlit app")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()

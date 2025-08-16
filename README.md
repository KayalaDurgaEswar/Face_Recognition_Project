
# Face Recognition Attendance System

A Python-based face recognition system for automated attendance tracking using computer vision and machine learning.

## Features

- **Face Detection**: Uses Haar Cascade Classifier for real-time face detection
- **Face Recognition**: K-Nearest Neighbors (KNN) algorithm for face recognition
- **Attendance Tracking**: Automated CSV-based attendance logging with timestamps
- **Web Interface**: Flask-based web application for easy interaction
- **Streamlit App**: Alternative Streamlit-based interface
- **Real-time Processing**: Live video capture and processing

## Project Structure

```
face_recognition_project/
├── data/                          # Data directory
│   ├── haarcascade_frontalface_default.xml  # Face detection model
│   ├── faces_data.pkl            # Trained face data (not in git)
│   ├── faces.pkl                 # Face encodings (not in git)
│   └── names.pkl                 # Name labels (not in git)
├── Attendance/                    # Attendance records (not in git)
├── static/                       # Static assets
├── templates/                    # HTML templates
├── add_faces.py                  # Face training script
├── test.py                       # Main face recognition script
├── web_app.py                    # Flask web application
├── app.py                        # Streamlit application
└── requirements.txt              # Python dependencies
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd face_recognition_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download required models:**
   - The Haar Cascade model is included in the `data/` directory
   - Face data files will be created when you train the system

## Usage

### 1. Training the System (Adding New Faces)

Run the face training script to add new people to the system:

```bash
python add_faces.py
```

- Enter the person's name when prompted
- The system will capture 100 face images
- Press 'q' to stop capturing
- Face data will be saved to `data/` directory

### 2. Running Face Recognition

#### Option A: Command Line Interface
```bash
python test.py
```

- Press 'o' to mark attendance
- Press 'q' to quit
- Attendance is automatically saved to CSV files

#### Option B: Web Application
```bash
python web_app.py
```

- Open browser and navigate to `http://localhost:5000`
- Use the web interface to manage faces and view attendance

#### Option C: Streamlit App
```bash
streamlit run app.py
```

- Opens a Streamlit interface in your browser
- View attendance records in real-time

### 3. Viewing Attendance Records

Attendance records are automatically saved in the `Attendance/` directory with the format:
- Filename: `Attendance_DD-MM-YYYY.csv`
- Columns: `NAME`, `TIME`

## Configuration

### Adding New People
1. Run `add_faces.py`
2. Enter the person's name
3. Capture face images (100 recommended)
4. The system automatically updates the training data

### Customizing Recognition
- Modify `KNeighborsClassifier(n_neighbors=5)` in the code to adjust recognition sensitivity
- Adjust face detection parameters in `facedetect.detectMultiScale()`

## Technical Details

- **Face Detection**: OpenCV Haar Cascade Classifier
- **Face Recognition**: Scikit-learn KNN Classifier
- **Image Processing**: OpenCV for image manipulation
- **Data Storage**: Pickle files for face data, CSV for attendance
- **Web Framework**: Flask for web interface, Streamlit for data visualization

## Dependencies

- OpenCV (`opencv-python`)
- NumPy
- Scikit-learn
- Flask
- Streamlit
- Pandas
- Pickle (built-in)

## Security Notes

- **Personal Data**: This repository excludes personal face data and attendance records
- **Model Files**: Trained models are not included in the repository
- **Privacy**: Ensure compliance with privacy laws when deploying

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please ensure you comply with all applicable laws and regulations when using this system for attendance tracking.

## Disclaimer

This system is for educational and demonstration purposes. Users are responsible for ensuring compliance with privacy laws and regulations in their jurisdiction.
=======
# Face_Recognition_Project
>>>>>>> 7398ef4abd959846c0ecfecf3529813ddd5dc2e6

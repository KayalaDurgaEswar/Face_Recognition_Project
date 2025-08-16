from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os
import cv2
import pickle
import numpy as np
import csv
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Global variables for face recognition
facedetect = None
knn = None
LABELS = None
FACES = None

def load_face_recognition_model():
    """Load the trained face recognition model"""
    global facedetect, knn, LABELS, FACES
    
    try:
        # Load face detection model
        facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        
        # Load trained data
        with open('data/names.pkl', 'rb') as w:
            LABELS = pickle.load(w)
        with open('data/faces_data.pkl', 'rb') as f:
            FACES = pickle.load(f)
        
        # Train KNN classifier
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(FACES, LABELS)
        
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def process_face_image(image_path):
    """Process a face image and return recognition result"""
    try:
        # Read image
        frame = cv2.imread(image_path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None, "No face detected"
        
        # Process the first detected face
        (x, y, w, h) = faces[0]
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        
        # Predict
        output = knn.predict(resized_img)
        return str(output[0]), "Success"
        
    except Exception as e:
        return None, f"Error processing image: {str(e)}"

def save_attendance(name):
    """Save attendance record to CSV"""
    try:
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        
        attendance_file = f"Attendance/Attendance_{date}.csv"
        attendance = [name, timestamp]
        
        # Check if file exists
        exist = os.path.isfile(attendance_file)
        
        if exist:
            with open(attendance_file, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            with open(attendance_file, "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['NAME', 'TIME'])
                writer.writerow(attendance)
        
        return True, f"Attendance recorded for {name} at {timestamp}"
    except Exception as e:
        return False, f"Error saving attendance: {str(e)}"

def capture_and_train_faces(name, images_data):
    """Capture 100 face images and train the model"""
    try:
        faces_data = []
        
        # Process each captured image
        for i, image_data in enumerate(images_data):
            # Decode base64 image
            import base64
            header, encoded = image_data.split(',', 1)
            data = base64.b64decode(encoded)
            
            # Save temporarily
            temp_path = os.path.join('data', f"temp_face_{i}.png")
            with open(temp_path, 'wb') as f:
                f.write(data)
            
            # Read and process image
            frame = cv2.imread(temp_path)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w, :]
                resized_img = cv2.resize(crop_img, (50, 50))
                faces_data.append(resized_img)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        if len(faces_data) < 50:  # Require at least 50 faces
            return False, f"Not enough faces detected. Got {len(faces_data)}, need at least 50."
        
        # Convert to numpy array
        faces_data = np.asarray(faces_data)
        faces_data = faces_data.reshape(faces_data.shape[0], -1)
        
        # Save to pickle files
        if 'names.pkl' not in os.listdir('data/'):
            names = [name] * len(faces_data)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
        else:
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            names = names + [name] * len(faces_data)
            with open('data/names.pkl', 'wb') as f:
                pickle.dump(names, f)
        
        if 'faces_data.pkl' not in os.listdir('data/'):
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces_data, f)
        else:
            with open('data/faces_data.pkl', 'rb') as f:
                faces = pickle.load(f)
            faces = np.append(faces, faces_data, axis=0)
            with open('data/faces_data.pkl', 'wb') as f:
                pickle.dump(faces, f)
        
        # Reload the model
        load_face_recognition_model()
        
        return True, f"Successfully trained model with {len(faces_data)} faces for {name}"
        
    except Exception as e:
        return False, f"Error training model: {str(e)}"

# Initialize face recognition model
if not load_face_recognition_model():
    print("Warning: Face recognition model could not be loaded!")

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Add face page
@app.route('/add_face', methods=['GET', 'POST'])
def add_face():
    if request.method == 'POST':
        data = request.get_json()
        if data and 'name' in data and 'images' in data:
            name = data['name']
            images = data['images']
            
            success, message = capture_and_train_faces(name, images)
            if success:
                return jsonify({'success': True, 'message': message})
            else:
                return jsonify({'success': False, 'message': message})
        else:
            return jsonify({'success': False, 'message': 'Invalid data received'})
    return render_template('add_face.html')

# Take attendance page
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    return render_template('attendance.html')

# Live attendance route (for AJAX calls)
@app.route('/live_attendance', methods=['POST'])
def live_attendance():
    try:
        # Get image data from request
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data received'})
        
        # Decode base64 image
        import base64
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        
        # Save temporarily
        temp_path = os.path.join('data', f"live_attendance_{int(time.time())}.png")
        with open(temp_path, 'wb') as f:
            f.write(image_bytes)
        
        # Process image
        name, status = process_face_image(temp_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if name:
            # Save attendance
            success, message = save_attendance(name)
            if success:
                return jsonify({'success': True, 'name': name, 'message': message})
            else:
                return jsonify({'success': False, 'message': message})
        else:
            return jsonify({'success': False, 'message': status})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# View/download attendance records
@app.route('/records')
def records():
    attendance_dir = os.path.join(os.getcwd(), 'Attendance')
    files = os.listdir(attendance_dir)
    files = [f for f in files if f.endswith('.csv')]
    return render_template('records.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    attendance_dir = os.path.join(os.getcwd(), 'Attendance')
    return send_from_directory(attendance_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 
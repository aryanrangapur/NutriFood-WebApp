from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
# import tensorflow as tf
import numpy as np
import base64
import io

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://aryanrangapur414:aryanbhai@cluster0.mbryk.mongodb.net/")
db = client['user_db']
users_collection = db['users']

# Load your trained food classification model
# model = tf.keras.models.load_model('path_to_your_model.h5')  # Replace with the actual model path

@app.route('/')
def index():
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again."
    
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = None  # Initialize error_message as None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        # Check if the user already exists
        if users_collection.find_one({'username': username}):
            error_message = "Username already exists. Try signing in."
            return render_template('signup.html', error_message=error_message)
        
        users_collection.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('signin'))
    
    return render_template('signup.html', error_message=error_message)

@app.route('/home', methods=['GET', 'POST'])
def home():
    prediction_result = None
    
    # If a POST request is made (form submission), process the image for classification
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                img = Image.open(file)
                prediction_result = predict_image(img)
    
    return render_template('home.html', prediction_result=prediction_result)

# Handle food classification via file upload
@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = secure_filename(file.filename)
        img = Image.open(file)
        prediction = predict_image(img)
        return f"Prediction: {prediction}"

# Handle food classification via camera input
@app.route('/classify-camera', methods=['POST'])
def classify_camera():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'prediction': None, 'error': 'No image data received'}), 400
    
    image_data = data['image']
    if not image_data:
        return jsonify({'prediction': None, 'error': 'Image data is empty'}), 400
    
    # Decode base64 image
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))

    prediction = predict_image(image)
    return jsonify({'prediction': prediction})



# Prediction helper function
def predict_image(image):
    # Preprocess the image to fit your model's input size
    img = image.resize((224, 224))  # Resize to the required size
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Predict using the model
    # prediction = model.predict(img)
    
    # Convert the prediction to readable label (e.g., food name)
    # label = np.argmax(prediction, axis=1)
    # Assuming you have a label map, e.g., {0: 'Pizza', 1: 'Burger'}
    label_map = {0: 'Pizza', 1: 'Burger'}  # Adjust according to your model classes
    # return label_map.get(label[0], "Unknown food")

if __name__ == '__main__':
    app.run(debug=True)

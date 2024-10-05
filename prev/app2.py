from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from tensorflow.keras.models import load_model
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
import numpy as np
import base64
import io
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://aryanrangapur414:aryanbhai@cluster0.mbryk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['user_db']
users_collection = db['users']


def custom_binary_crossentropy(*args, **kwargs):
    return tf.keras.losses.BinaryCrossentropy()

# Load your trained food classification model
model = load_model('food_CNN.h5', custom_objects={'BinaryCrossentropy': custom_binary_crossentropy})
  # Replace with the actual model path

# Define the label map for your food classification model (this should match the class indices of your model)
def load_and_pred(model, img,class_names):
    img = tf.image.resize(img, size=[224, 224])
    img = img / 255.0

    prediction = model.predict(tf.expand_dims(img, axis=0))
    predicted_class = class_names[int(tf.round(prediction))]

    return predicted_class

@app.route('/')
def index():
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('home'))
        else:
            error_message = "Invalid credentials. Try again."
    
    return render_template('signin.html', error_message=error_message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = None
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
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Save the image to display later
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                
                # Make prediction on the image
                prediction = predict_image(filepath)
                
                # Redirect to result page with image path and prediction result
                return redirect(url_for('result', image_url=filepath, prediction=prediction))
    
    return render_template('home.html')

@app.route('/result')
def result():
    image_url = request.args.get('image_url')
    prediction = request.args.get('prediction')
    
    return render_template('result.html', image_url=image_url, prediction=prediction)

# Prediction helper function
def predict_image(filepath):
    # Preprocess the image to fit your model's input size
    img = Image.open(filepath)
    img = img.resize((224, 224))  # EfficientNetB0 expects 224x224 input
    img = np.array(img) / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Predict using the loaded EfficientNetB0 model
    prediction = model.predict(img)
    
    # Convert the prediction to a readable label (e.g., food name)
    label = np.argmax(prediction, axis=1)
    
    # Return the food label from the label map
    return label_map.get(label[0], "Unknown food")

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(host='0.0.0.0', port=5000, debug=True)

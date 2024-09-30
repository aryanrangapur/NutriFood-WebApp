from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
import numpy as np
import base64
import io
import os

app = Flask(__name__)

class_names = ["Pizza", "Steak"]

# MongoDB connection
client = MongoClient("mongodb+srv://aryanrangapur414:aryanbhai@cluster0.mbryk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['user_db']
users_collection = db['users']

def custom_binary_crossentropy(*args, **kwargs):
    return tf.keras.losses.BinaryCrossentropy()


model = tf.keras.models.load_model('food_CNN.h5', custom_objects={'BinaryCrossentropy': custom_binary_crossentropy})

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
    prediction_result = None
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                try:
                    img = Image.open(file)
                    prediction_result = predict_image(model=model, img=img, class_names=class_names)
                except OSError:
                    return render_template('home.html', prediction_result="This file type is not allowed.")
    
    return render_template('home.html', prediction_result=prediction_result)

import base64

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    # validate file type
    if not allowed_file(file.filename):
        return render_template('result.html', prediction="This file type is not allowed.")

    try:
        img = Image.open(file.stream)

        # convert image to base64 to pass it to the template 
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        prediction = predict_image(model, img, class_names)

        # result page with the prediction and the image
        return render_template('result.html', prediction=prediction, img_data=img_base64)
    except OSError:
        return render_template('result.html', prediction="This file type is not allowed.") #for diff types of files


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

    prediction = predict_image(model=model, img=image, class_names=class_names)
    return jsonify({'prediction': prediction})

# allowable formats
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# rgba to rgb, no error in model 4->3
def predict_image(model, img, class_names):
    if img.mode == 'RGBA':
        img = img.convert('RGB')  

    img = tf.image.resize(np.array(img), size=[224, 224])  
    img = img / 255.0  # Normalize the image
    prediction = model.predict(tf.expand_dims(img, axis=0)) 
    predicted_class = class_names[int(tf.round(prediction))]

    return predicted_class

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

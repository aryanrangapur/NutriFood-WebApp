from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import tensorflow as tf
import numpy as np
import base64
import io
import os
import requests

app = Flask(__name__)

class_names = ["Pizza", "Steak"]

# MongoDB connection
client = MongoClient("mongodb+srv://aryanrangapur414:aryanbhai@cluster0.mbryk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['user_db']
users_collection = db['users']

# Edamam API credentials
EDAMAM_API_ID = '06d64f3c'
EDAMAM_API_KEY = '30de0c0e7353addf15f68fdce6d73005'
EDAMAM_API_URL = 'https://api.edamam.com/api/nutrition-data'

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
        
        if users_collection.find_one({'username': username}):
            error_message = "Username already exists. Try signing in."
            return render_template('signup.html', error_message=error_message)
        
        users_collection.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('signin'))
    
    return render_template('signup.html', error_message=error_message)

@app.route('/home', methods=['GET', 'POST'])
def home():
    prediction_result = None
    nutrition_info = None
    img_base64 = None  # Initialize img_base64 here

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                try:
                    img = Image.open(file)
                    prediction_result = predict_image(model=model, img=img, class_names=class_names)

                    # Convert image to base64 to display on the result page
                    img_io = io.BytesIO()
                    img.save(img_io, format='JPEG')
                    img_io.seek(0)
                    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

                    # Fetch nutrition information based on the prediction result
                    nutrition_info = get_nutrition_info(prediction_result)

                except OSError:
                    return render_template('home.html', prediction_result="This file type is not allowed.")
    
    return render_template('home.html', prediction_result=prediction_result, nutrition_info=nutrition_info, img_data=img_base64)

@app.route('/fetch_nutrition_with_quantity', methods=['POST'])
def fetch_nutrition_with_quantity():
    food_item = request.form['food_item']
    quantity = request.form['quantity']

    # Fetch nutrition information based on the prediction result and the quantity
    nutrition_info = get_nutrition_info(food_item, quantity)

    return render_template('result.html', prediction=food_item, nutrition_info=nutrition_info, img_data=request.form['img_data'])

def get_nutrition_info(food_item, quantity=None):
    params = {
        'app_id': EDAMAM_API_ID,
        'app_key': EDAMAM_API_KEY,
        'ingr': f"{quantity} g {food_item}" if quantity else food_item  
    }

    response = requests.get(EDAMAM_API_URL, params=params)

    if response.status_code == 200:
        nutrition_data = response.json()
        
        calories = nutrition_data.get('calories', 'N/A')
        total_weight = nutrition_data.get('totalWeight', 'N/A')
        diet_labels = nutrition_data.get('dietLabels', [])
        health_labels = nutrition_data.get('healthLabels', [])
        
        meal_type = nutrition_data.get('mealType', 'N/A')
        dish_type = nutrition_data.get('dishType', 'N/A')
        cuisine_type = nutrition_data.get('cuisineType', 'N/A')
        nutrients = nutrition_data.get('totalNutrients', {})

        return {
            'calories': calories,
            'total_weight': total_weight,
            'diet_labels': [label.lower().replace('_', ' ') for label in diet_labels],
            'health_labels': [label.lower().replace('_', ' ') for label in health_labels],
            'meal_type': meal_type,
            'dish_type': dish_type,
            'cuisine_type': cuisine_type,
            'nutrients': {key.lower().replace('_', ' '): value for key, value in nutrients.items()}
    
        }
    else:
        return None


@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if not allowed_file(file.filename):
        return render_template('result.html', prediction="This file type is not allowed.")

    try:
        img = Image.open(file.stream)

        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        prediction = predict_image(model, img, class_names)

        nutrition_info = get_nutrition_info(prediction)

        # Result page with the prediction and the image
        return render_template('result.html', prediction=prediction, img_data=img_base64, nutrition_info=nutrition_info)
    except OSError:
        return render_template('result.html', prediction="This file type is not allowed.")

@app.route('/classify-camera', methods=['POST'])
def classify_camera():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'prediction': None, 'error': 'No image data received'}), 400
    
    image_data = data['image']
    if not image_data:
        return jsonify({'prediction': None, 'error': 'Image data is empty'}), 400
    
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))

    prediction = predict_image(model=model, img=image, class_names=class_names)

    nutrition_info = get_nutrition_info(prediction)
    
    return jsonify({'prediction': prediction, 'nutrition_info': nutrition_info})

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# RGBA to RGB, no error in model 4->3
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
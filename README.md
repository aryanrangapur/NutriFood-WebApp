

# NutriFood

A web application for **food classification** powered by a Convolutional Neural Network (CNN). Users can upload images of food or capture photos using their device camera, and the application predicts the type of food. After classification, the app also fetches **nutritional insights** (proteins, vitamins, minerals, and recommendations on when to consume or avoid the food) through an API integration.

## Features

* **User Authentication**: Sign up and sign in with secure password storage using MongoDB.
* **Image Classification**: Upload food images or capture them directly from the camera for instant classification.
* **Camera Upload**: Capture photos on the go for predictions without manual file selection.
* **Real-time Predictions**: Receive instant results on uploaded or captured food images.
* **Nutritional Insights**: After classification, the app calls an API to provide detailed nutrition information (proteins, vitamins, minerals) and suggestions on when the food is beneficial or not.
* **Secure Passwords**: Passwords are hashed before being stored in MongoDB for enhanced security.

## Tech Stack

* **Backend**: Flask (Python)
* **Frontend**: HTML, CSS (Jinja templates)
* **Machine Learning Model**: TensorFlow, Keras (CNN)
* **Database**: MongoDB (user authentication and storage)
* **Image Processing**: Pillow (PIL)
* **Deployment**: AWS EC2 (temporarily paused at `http://13.60.217.221/`)

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/aryanrangapur/NutriFood-WebApp.git
   ```

2. Navigate to the project directory:

   ```bash
   cd NutriFood-WebApp
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:

   ```bash
   python app3.py
   ```

5. Open the application in your browser:

   * Local: `http://localhost:5000`
   * Deployment (when live): `http://13.60.217.221/`

## Usage

* **Sign Up**: Register a new account to start using the app.
* **Sign In**: Log in with your credentials.
* **Upload Image**: Upload a food image for classification.
* **Use Camera**: Capture a photo from your device camera and classify it.
* **Get Nutritional Insights**: After prediction, the app fetches detailed nutrition data and provides recommendations on food consumption.

## Model

The core model is a **Convolutional Neural Network (CNN)** trained with TensorFlow to classify food into predefined categories. Predictions are enriched with additional nutritional insights through an API integration.

## Future Improvements

* Expand the number of supported food categories.
* Improve UI/UX for smoother interaction.
* Enhance prediction accuracy by training on larger, more diverse datasets.
* Add personalized diet recommendations based on user health goals.


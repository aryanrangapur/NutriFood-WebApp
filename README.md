# NutriFood 

A web application for food classification using machine learning models. Users can upload images of food or take pictures using their camera, and the application will predict the type of food using a trained CNN model.

## Features

- **User Authentication**: Sign up and sign in functionality using MongoDB for user storage.
- **Image Classification**: Upload food images or use the camera to classify images into categories like Pizza and Steak.
- **Camera Upload**: Take a photo from your device and get a prediction.
- **Real-time Predictions**: Get instant feedback on uploaded images.
- **Secure Passwords**: Passwords are hashed and stored securely in MongoDB.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Jinja templates)
- **Machine Learning Model**: TensorFlow, Keras (CNN)
- **Database**: MongoDB (for user authentication)
- **Image Processing**: Pillow (PIL)
- **Deployment**: Can be deployed locally or on a cloud platform.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/aryanrangapur/ML-WEB.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ML-WEB
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:
    ```bash
    python app.py
    ```

5. Open a browser and navigate to `http://localhost:5000` to access the application.

## Usage

- **Sign Up**: Create an account to start classifying images.
- **Sign In**: Log in with your credentials.
- **Upload Image**: Use the 'Upload' button to classify an image from your device.
- **Use Camera**: Take a picture using your device's camera and get a prediction.

## Model

The classification model is a Convolutional Neural Network (CNN) trained using TensorFlow. It classifies food images into predefined categories.

## Future Improvements

- Add more food categories.
- Improve UI/UX for better user interaction.
- Enhance prediction accuracy by training on more diverse datasets.




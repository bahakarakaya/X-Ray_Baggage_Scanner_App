from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid
from model_handler import YOLOModel

# initializes Flask app
app = Flask(__name__)
CORS(app)

# create uploads folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLOModel("models/xray_model_- 18 may 2025 16_32.pt")

@app.route('/')
def home():
    return "X-Ray API is working!"

# This endpint, gets an image from the user, process and answer
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': "Image couldn't be uploaded."}), 400

    file = request.files['image']

    # save file with a unique id
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    print(f"Saved file to: {filepath}, size: {os.path.getsize(filepath)} bytes")

    try:
        result = model.predict(filepath)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            os.remove(filepath)
            print("deleted?")
        except Exception as remove_err:
            print(f"Failed to delete file: {filepath}, error: {remove_err}")

    return jsonify(result)

# Starts Flask app
if __name__ == '__main__':
    app.run(debug=True)
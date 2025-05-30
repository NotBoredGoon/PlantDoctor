from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import backend

app = Flask(__name__)
CORS(app)  # This will allow requests from your React frontend

# Ensure an 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route('/api/process_image', methods=['POST'])
def handle_process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    zip_code = request.form.get('zip_code')
    image_file = request.files['image']

    if not zip_code:
        return jsonify({"error": "No zip code provided"}), 400

    # Save the uploaded image to the 'uploads' directory
    image_path = os.path.join('uploads', image_file.filename)
    image_file.save(image_path)

    # Call your backend processing function
    result_text = backend.process_image(zip_code, image_path)

    return jsonify({"text": result_text})

if __name__ == '__main__':
    app.run(debug=True)
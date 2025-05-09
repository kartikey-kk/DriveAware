from flask import Flask, request
import requests
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

CLOUD_NAME = 'dclq31q8y'
UPLOAD_PRESET = 'esp32upload'
CLOUDINARY_URL = f'https://api.cloudinary.com/v1_1/{CLOUD_NAME}/image/upload'

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return {"status": "fail", "message": "No file part"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"status": "fail", "message": "No selected file"}, 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'upload_preset': UPLOAD_PRESET}
            response = requests.post(CLOUDINARY_URL, data=data, files=files)

        os.remove(file_path)  # cleanup

        if response.status_code == 200:
            image_url = response.json().get('secure_url')
            return {"status": "success", "url": image_url}, 200
        else:
            return {"status": "fail", "message": response.text}, 500

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

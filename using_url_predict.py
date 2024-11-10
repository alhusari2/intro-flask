import os
import requests
from flask import Flask, jsonify, request
from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
from huggingface_hub import login
from io import BytesIO
from PIL import Image  # Untuk memuat gambar dari stream byte
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
auth_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
login(auth_token)
processor = AutoImageProcessor.from_pretrained("Libidrave/BlurorBokehv1.1", token=auth_token)
model = AutoModelForImageClassification.from_pretrained("Libidrave/BlurorBokehv1.1", token=auth_token)

app = Flask(__name__)
upload_folder = 'static/uploads'
# Buat folder upload jika belum ada
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder


@app.route('/predict/', methods=['POST'])
def predict():
    data = request.get_json()

    if data and 'url' in data:
        image_url = data['url']
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            resized_image = image.resize((224, 224))
            # Menyimpan gambar yang diunduh dan di-resize
            file_path = os.path.join(upload_folder, "downloaded_image.jpg")
            resized_image.save(file_path)  # Menyimpan gambar ke folder upload

            inputs = processor(images=resized_image, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits
            predictions = logits.softmax(dim=1)
            score, label = predictions[0].max(0)

            return jsonify({
                'status':{
                    'code': 200,
                    'message': 'Success'
                },
                'data':{
                    "score": score.item(),
                    "label": label.item()
                }
            })

        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 400    
        
if __name__ == "__main__":
    app.run(debug=True)

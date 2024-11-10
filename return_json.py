import os
import torch
from flask import Flask, jsonify, request, render_template
from transformers import pipeline
from huggingface_hub import login
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
auth_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
login(auth_token)

def prediction(input_image_path):
    """
    Fungsi untuk melakukan prediksi dari FineTuned Model menggunakan
    High Level API Transformers
    """
    pipe = pipeline("image-classification", model="Libidrave/BlurorBokehv1.1")

    predictions = pipe(input_image_path, function_to_apply='softmax')
    score = predictions[0]["score"]
    label = predictions[0]["label"]
    return score, label

app = Flask(__name__)
upload_folder = 'static/uploads'

# Buat folder upload jika belum ada
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/')
def index():
    return render_template('introduction.html')

@app.route('/predict/', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({
                "message": "No file found"
            }), 400
        
        file = request.files['file']
        file_allowed = ['jpg', 'jpeg', 'png']
        
        if file.filename == '':
            return jsonify({
                "message": "No file selected for uploading"
            }), 400
        
        if not (file.filename.split('.')[-1].lower() in file_allowed):
            return jsonify({
                "message": "Invalid file format. Only .jpg, .jpeg, .png are allowed"
            }), 400
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        try:
            score, label = prediction(file_path)
            return jsonify({
                "score": score,
                "label": label
            })
            
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 500
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
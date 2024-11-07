from flask import Flask, jsonify, request
from transformers import pipeline
from huggingface_hub import login
import os
from dotenv import load_dotenv
import torch

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

@app.route('/predict/', methods=['GET','POST'])
def predict():
  if request.method == 'POST':
    # cek file yang diupload harus jpg, jpeg, atau png
    if 'file' not in request.files:
      return jsonify({
        "message": "No file found"
        }),400
    
    file = request.files['file']
    # Cek file yang diupload harus jpg, jpeg, atau png
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
           "score": score, "label": label
           })
        
    except Exception as e:
        return jsonify({
           "message": str(e)
           }), 500
    

if __name__ == '__main__':
    app.run(debug=True)
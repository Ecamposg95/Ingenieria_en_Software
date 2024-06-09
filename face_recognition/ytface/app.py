import os
import datetime
import cv2
import base64
from flask import Flask, jsonify, request, render_template, redirect, url_for
import face_recognition
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')

# Crear variable de registro
registered_data = {}

def decode_image(data_url):
    header, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    image = Image.open(BytesIO(data))
    return image

@app.route('/')
def index():
    # Renderizar archivo HTML
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    photo_data_url = data.get('photo')
    if photo_data_url and name:
        uploads_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)
        
        # Decodificar y guardar la foto
        image = decode_image(photo_data_url)
        filename = f"{datetime.date.today()}_{name}.jpg"
        filepath = os.path.join(uploads_folder, filename)
        image.save(filepath)
        
        # Registrar la cara
        image = face_recognition.load_image_file(filepath)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            registered_data[name] = encoding[0]
            return jsonify({"message": "Registro exitoso"}), 200
    return jsonify({"message": "Error en el registro"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    photo_data_url = data.get('photo')
    if photo_data_url:
        uploads_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)
        
        # Decodificar y guardar la foto del login
        image = decode_image(photo_data_url)
        login_filename = os.path.join(uploads_folder, "login_face.jpg")
        image.save(login_filename)
        
        # Detectar si hay una cara en la imagen
        login_image = cv2.imread(login_filename)
        gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            response = {"success": False}
            return jsonify(response)
        
        # Procesar el reconocimiento facial
        login_image = face_recognition.load_image_file(login_filename)
        login_face_encodings = face_recognition.face_encodings(login_image)
        
        if len(login_face_encodings) > 0:
            login_face_encoding = login_face_encodings[0]
            for name, registered_face_encoding in registered_data.items():
                matches = face_recognition.compare_faces([registered_face_encoding], login_face_encoding)
                if any(matches):
                    response = {"success": True, "name": name}
                    return jsonify(response)
        
        response = {"success": False}
        return jsonify(response)
    return redirect(request.url)

@app.route('/success')
def success():
    user_name = request.args.get('user_name')
    return render_template('success.html', user_name=user_name)

if __name__ == '__main__':
    app.run(debug=True)


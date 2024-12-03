from flask import Flask, jsonify, send_file, Response
from pydub import AudioSegment
import os
import subprocess
from threading import Thread
import time

# Configuración del servidor Flask
app = Flask(__name__)

# Ruta donde se almacenarán los archivos de audio
UPLOAD_FOLDER = '/data/data/com.termux/files/home/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variables para simular estados
state = {
    "food_container_open": False,
    "water_container_open": False,
    "toy_active": False
}

@app.route('/open_food', methods=['GET'])
def open_food():
    state["food_container_open"] = True
    return jsonify({"message": "Contenedor de comida abierto"}), 200

@app.route('/open_water', methods=['GET'])
def open_water():
    state["water_container_open"] = True
    return jsonify({"message": "Contenedor de agua abierto"}), 200

@app.route('/activate_toy', methods=['POST'])
def activate_toy():
    state["toy_active"] = True
    return jsonify({"message": "Juguete activado"}), 200



@app.route('/download_audio/<filename>', methods=['GET'])
def download_audio(filename):
    """Descargar el archivo convertido a MP3."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Archivo no encontrado"}), 404

@app.route('/convert_audio', methods=['POST'])
def convert_audio():
    ogg_file = os.path.join(UPLOAD_FOLDER, 'audio.ogg')
    mp3_file = os.path.join(UPLOAD_FOLDER, 'audio.mp3')

    if not os.path.exists(ogg_file):
        return jsonify({"error": "Archivo OGG no encontrado"}), 404

    try:
        # Convertir el archivo a MP3
        audio = AudioSegment.from_file(ogg_file, format="ogg")
        audio.export(mp3_file, format="mp3")

        # Reproducir el archivo usando Termux API
        subprocess.run(['termux-media-player', 'play', mp3_file], check=True)

        return jsonify({"message": "Archivo convertido y reproducido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Ruta para almacenar capturas temporales de la cámara
CAPTURE_PATH = '/data/data/com.termux/files/home/capture.jpg'

@app.route('/video_feed', methods=['GET'])
def video_feed():
    """Proporciona un flujo de video en tiempo real."""
    def generate_frames():
        while True:
            try:
                # Captura una imagen de la cámara de Termux
                subprocess.run(['termux-camera-photo', CAPTURE_PATH], check=True)
                with open(CAPTURE_PATH, 'rb') as img:
                    frame = img.read()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.1)  # Ajusta la frecuencia de captura según sea necesario
            except Exception as e:
                break
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(host='127.0.0.1', port=5000)

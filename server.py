from flask import Flask, jsonify, send_file
from pydub import AudioSegment
import os

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
    """Convertir archivo OGG a MP3."""
    # Esperamos que el cliente especifique el archivo a convertir
    ogg_file = os.path.join(UPLOAD_FOLDER, 'audio.ogg')
    mp3_file = os.path.join(UPLOAD_FOLDER, 'audio.mp3')

    if not os.path.exists(ogg_file):
        return jsonify({"error": "Archivo OGG no encontrado"}), 404

    try:
        # Convertir el archivo a MP3
        audio = AudioSegment.from_file(ogg_file, format="ogg")
        audio.export(mp3_file, format="mp3")
        return jsonify({"message": "Archivo convertido", "download_url": f"/download_audio/audio.mp3"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(host='127.0.0.1', port=5000)

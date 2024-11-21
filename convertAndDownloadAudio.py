import subprocess
from flask import Flask, jsonify, send_file
from pydub import AudioSegment
import os

# Configuración del servidor Flask
app = Flask(__name__)

# Ruta donde se almacenarán los archivos de audio
UPLOAD_FOLDER = '/data/data/com.termux/files/home/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert_audio', methods=['POST'])
def convert_audio():
    """Convertir archivo OGG a MP3 y reproducirlo."""
    ogg_file = os.path.join(UPLOAD_FOLDER, 'audio.ogg')
    mp3_file = os.path.join(UPLOAD_FOLDER, 'audio.mp3')

    if not os.path.exists(ogg_file):
        return jsonify({"error": "Archivo OGG no encontrado"}), 404

    try:
        # Convertir el archivo a MP3
        audio = AudioSegment.from_file(ogg_file, format="ogg")
        audio.export(mp3_file, format="mp3")

        # Reproducir el archivo MP3
        subprocess.run(['play', mp3_file], check=True)  # Usa 'play' de SoX
        # Alternativamente, usa MPV:
        # subprocess.run(['mpv', mp3_file], check=True)

        return jsonify({"message": "Archivo convertido y reproducido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ejecutar el servidor Flask
    app.run(host='127.0.0.1', port=5000)

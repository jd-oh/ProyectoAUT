import requests
import os

# Configuración
SERVER_URL = 'http://127.0.0.1:5000'  # Cambia si el servidor Flask está en otro host
UPLOAD_FOLDER = '/data/data/com.termux/files/home/uploads'
OGG_FILE = os.path.join(UPLOAD_FOLDER, 'audio.ogg')
MP3_FILE = os.path.join(UPLOAD_FOLDER, 'audio.mp3')

def upload_and_convert_audio():
    """Sube el archivo OGG al servidor y solicita la conversión a MP3."""
    # Verificar si el archivo OGG existe
    if not os.path.exists(OGG_FILE):
        print(f"El archivo {OGG_FILE} no existe. Asegúrate de que esté disponible.")
        return

    try:
        # Enviar solicitud de conversión
        print("Solicitando conversión del archivo OGG a MP3...")
        response = requests.post(f"{SERVER_URL}/convert_audio")
        if response.status_code == 200:
            data = response.json()
            download_url = data.get("download_url")
            print("Conversión exitosa. Descargando MP3...")
            
            # Descargar el archivo MP3
            download_response = requests.get(f"{SERVER_URL}{download_url}")
            if download_response.status_code == 200:
                with open(MP3_FILE, 'wb') as mp3_file:
                    mp3_file.write(download_response.content)
                print(f"Archivo MP3 descargado en: {MP3_FILE}")
            else:
                print("Error al descargar el archivo MP3.")
        else:
            print(f"Error en la conversión: {response.json().get('error')}")
    except Exception as e:
        print(f"Error durante la conversión o descarga: {str(e)}")

if __name__ == "__main__":
    upload_and_convert_audio()

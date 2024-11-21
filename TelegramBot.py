# Importar las bibliotecas necesarias
import telebot
import requests
import subprocess
from flask import Flask, jsonify, request
from threading import Thread

# Configuración del bot de Telegram
BOT_TOKEN = '7814318271:AAGeY5_LcIwpt2h-anr-7NDTi5u_Cyik0cI'
bot = telebot.TeleBot(BOT_TOKEN)

# Configuración del servidor Flask
app = Flask(__name__)

# Variables para simular estados
state = {
    "food_container_open": False,
    "water_container_open": False,
    "toy_active": False
}

# Rutas del servidor Flask
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

# Funciones del bot de Telegram
@bot.message_handler(commands=['menu'])
def send_menu(message):
    # Crear un teclado inline con las opciones que necesitas
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Tomar foto', callback_data='take_photo'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Abrir contenedor de comida', callback_data='open_food'),
        telebot.types.InlineKeyboardButton('Abrir contenedor de agua', callback_data='open_water')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Activar juguete', callback_data='activate_toy')
    )
    # Enviar el menú al usuario
    bot.send_message(message.chat.id, 'Selecciona una opción:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'take_photo':
        # Responder rápidamente al callback query
        bot.answer_callback_query(call.id, 'Procesando...')
        # Llamar a la función para tomar la foto en un subproceso
        Thread(target=tomar_foto_y_enviar, args=(call,)).start()

    elif call.data == 'open_food':
        # Hacer una petición GET al servidor Flask
        response = requests.get('http://127.0.0.1:5000/open_food')
        if response.status_code == 200:
            bot.answer_callback_query(call.id, 'Contenedor de comida abierto.')
        else:
            bot.answer_callback_query(call.id, f'Error: {response.text}')

    elif call.data == 'open_water':
        # Hacer una petición GET al servidor Flask
        response = requests.get('http://127.0.0.1:5000/open_water')
        if response.status_code == 200:
            bot.answer_callback_query(call.id, 'Contenedor de agua abierto.')
        else:
            bot.answer_callback_query(call.id, f'Error: {response.text}')

    elif call.data == 'activate_toy':
        # Hacer una petición POST al servidor Flask
        response = requests.post('http://127.0.0.1:5000/activate_toy')
        if response.status_code == 200:
            bot.answer_callback_query(call.id, 'Juguete activado.')
        else:
            bot.answer_callback_query(call.id, f'Error: {response.text}')

def tomar_foto_y_enviar(call):
    """Función para tomar una foto y enviarla en un subproceso."""
    try:
        # Ruta donde se guardará la foto
        photo_path = '/data/data/com.termux/files/home/foto.jpg'
        # Tomar la foto usando la cámara de Termux
        subprocess.run(['termux-camera-photo', photo_path], check=True)
        # Enviar la foto al usuario
        with open(photo_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption="¡Aquí está tu foto!")
    except Exception as e:
        # Notificar al usuario si ocurre un error
        bot.send_message(call.message.chat.id, f'Error al tomar la foto: {str(e)}')

# Función para ejecutar el bot y el servidor Flask
def start():
    # Iniciar el bot en un hilo separado
    Thread(target=lambda: bot.polling()).start()
    # Ejecutar el servidor Flask
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    start()

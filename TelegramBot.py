import telebot
import requests
import subprocess
from threading import Thread

# Configuración del bot de Telegram
BOT_TOKEN = '7814318271:AAGeY5_LcIwpt2h-anr-7NDTi5u_Cyik0cI'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['menu'])
def send_menu(message):
    # Crear un teclado inline con las opciones necesarias
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
        # Ejecutar la tarea de tomar foto en un subproceso
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
    """Función para tomar una foto y enviarla."""
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

if __name__ == '__main__':
    # Iniciar el bot
    bot.polling()

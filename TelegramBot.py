import telebot
import requests
import subprocess
from threading import Thread
import os

# Configuración del bot de Telegram
BOT_TOKEN = '7814318271:AAGeY5_LcIwpt2h-anr-7NDTi5u_Cyik0cI'
bot = telebot.TeleBot(BOT_TOKEN)

UPLOAD_FOLDER = '/data/data/com.termux/files/home/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
        bot.answer_callback_query(call.id, 'Procesando...')
        Thread(target=tomar_foto_y_enviar, args=(call,)).start()

def tomar_foto_y_enviar(call):
    try:
        photo_path = '/data/data/com.termux/files/home/foto.jpg'
        subprocess.run(['termux-camera-photo', photo_path], check=True)
        with open(photo_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption="¡Aquí está tu foto!")
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Error al tomar la foto: {str(e)}')

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    """Manejar mensajes de audio (voice)."""
    try:
        # Obtener la información del archivo de audio
        file_info = bot.get_file(message.voice.file_id)
        # Descargar el archivo
        downloaded_file = bot.download_file(file_info.file_path)
        # Guardar el archivo como audio.ogg
        ogg_path = os.path.join(UPLOAD_FOLDER, 'audio.ogg')
        with open(ogg_path, 'wb') as audio_file:
            audio_file.write(downloaded_file)

        # Confirmar al usuario
        bot.reply_to(message, "¡Audio recibido y guardado! Listo para convertir.")
    except Exception as e:
        bot.reply_to(message, f"Error al procesar el audio: {str(e)}")

if __name__ == '__main__':
    bot.polling()

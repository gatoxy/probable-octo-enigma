import requests
import telebot
import os
import psycopg2
from io import BytesIO

# Chave da API do Telegram
CHAVE_API = "7111668089:AAHcJZrbuUnJjuSxwNlx0cED_iiYdtp03Mc"

# Configurações do banco de dados PostgreSQL
DB_HOST = 'dpg-coodqu2cn0vc738n8rt0-a'
DB_NAME = 'dbtelebot'
DB_USER = 'dbtelebot'
DB_PASSWORD = 'WXNB1epZt6ATjbQq1pu6etxNrwuSjQRT'

# Estabelece conexão com o bot do Telegram
bot = telebot.TeleBot(CHAVE_API)

# Função para conectar ao banco de dados PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Manipuladores de mensagens
@bot.message_handler(commands=['start'])
def send_begin(message):
    bot.reply_to(
        message, 
        f"Olá {message.from_user.first_name}, sou o Bot Roxa e estou aqui para te ajudar. Como posso te ajudar?\n\n"
        "/baixar: Baixe vídeos de qualquer link"
    )

@bot.message_handler(commands=['baixar'])
def send_download(message):
    bot.send_message(
        message.chat.id, 
        "Por favor, cole o link do vídeo que você deseja baixar."
    )

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    try:
        bot.send_message(message.chat.id, 'Estou baixando o vídeo...')

        # Simulando o download do vídeo
        video_url = message.text
        video_request = requests.get(video_url)
        video_data = video_request.content

        # Conectando ao banco de dados
        connection = connect_to_db()
        cursor = connection.cursor()

        # Inserindo os dados do vídeo no banco de dados
        cursor.execute("INSERT INTO videos (dados) VALUES (%s) RETURNING id", (psycopg2.Binary(video_data),))
        video_id = cursor.fetchone()[0]
        connection.commit()

        bot.send_message(message.chat.id, 'Vídeo baixado com sucesso!')

        # Enviando o vídeo de volta para o usuário
        video_file = BytesIO(video_data)
        video_file.name = 'video.mp4'
        bot.send_video(message.chat.id, video_file)

        # Fechando a conexão com o banco de dados
        cursor.close()
        connection.close()

    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro ao tentar baixar e armazenar o vídeo: {str(e)}")

# Inicia a escuta de mensagens
bot.infinity_polling()

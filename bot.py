import telebot
import os
import psycopg2

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

        # Baixando vídeo pelo link
        video_url = message.text

        # Simulando o download do vídeo
        video_filename = video_url.split('/')[-1]
        video_filepath = f'/path/to/your/local/directory/{video_filename}'

        # Lendo o arquivo de vídeo como bytes
        with open(video_filepath, 'rb') as video_file:
            video_data = video_file.read()

        # Conectando ao banco de dados
        connection = connect_to_db()
        cursor = connection.cursor()

        # Inserindo o arquivo no banco de dados
        cursor.execute("INSERT INTO videos (nome, dados) VALUES (%s, %s)", (video_filename, video_data))
        connection.commit()

        bot.send_message(message.chat.id, 'Vídeo baixado com sucesso!')

        # Enviando mensagem de confirmação
        bot.send_message(message.chat.id, 'O vídeo foi baixado e armazenado com sucesso no banco de dados.')

        # Fechando a conexão com o banco de dados
        cursor.close()
        connection.close()

    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro ao tentar baixar e armazenar o vídeo: {str(e)}")

# Inicia a escuta de mensagens
bot.infinity_polling()

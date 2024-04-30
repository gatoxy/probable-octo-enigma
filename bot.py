import telebot
import requests
import os
import tempfile

# Chave da API do Telegram
CHAVE_API = "6914169408:AAF8iQV53vASbKiDHl7H2vRRLcDb85VhPqc"

# Estabelece conexão com o bot do Telegram
bot = telebot.TeleBot(CHAVE_API)

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
        video_request = requests.get(video_url)
        video_filename = video_url.split('/')[-1]

        # Salvar o arquivo temporário no diretório temporário do sistema
        temp_directory = tempfile.gettempdir()
        video_filepath = os.path.join(temp_directory, video_filename)
        
        with open(video_filepath, 'wb') as video_file:
            video_file.write(video_request.content)

        bot.send_message(message.chat.id, 'Vídeo baixado com sucesso!')

        # Enviando o vídeo
        with open(video_filepath, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

        # Removendo o arquivo temporário após o envio
        os.remove(video_filepath)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro ao tentar baixar e enviar o vídeo: {str(e)}")

# Inicia a escuta de mensagens
bot.infinity_polling()

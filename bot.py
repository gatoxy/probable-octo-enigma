import requests
import threading
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler

# Estados
LINK_INPUT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Olá {user_name}, seja bem-vindo ao bot stream!!")
    await update.message.reply_text("Para baixar arquivos, aperte em /download.")
    return ConversationHandler.END

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Por favor, envie o link para o vídeo MP4 que deseja baixar.")
    return LINK_INPUT

async def download_file(link, chat_id, context):
    loop = asyncio.get_running_loop()
    # Fazendo solicitação GET para o link do vídeo
    response = requests.get(link, stream=True)

    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Enviando o vídeo como uma mensagem de documento (MP4) para o bot do Telegram
        document_content = b''
        for chunk in response.iter_content(chunk_size=8192):  # Ajuste o tamanho do chunk conforme necessário
            document_content += chunk
            # Enviando mensagem de progresso a cada 20 segundos
            if len(document_content) % (20 * 1024 * 1024) == 0:
                await loop.run_in_executor(None, context.bot.send_message, chat_id, f"Baixando... Tamanho atual: {len(document_content)//1024} KB")
        await context.bot.send_message(chat_id, "Iniciando o download...")
        await context.bot.send_document(chat_id, document=document_content, filename="video.mp4")
        await context.bot.send_message(chat_id, "Download concluído!")
    else:
        await context.bot.send_message(chat_id, "Ocorreu um erro ao baixar o vídeo. Por favor, tente novamente.")

async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.effective_user.first_name
    link = update.message.text
    await update.message.reply_text("Iniciando o download...")

    # Iniciando uma thread para baixar o arquivo
    threading.Thread(target=lambda: asyncio.run(download_file(link, update.message.chat_id, context))).start()

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("download", download)],
    states={
        LINK_INPUT: [MessageHandler(None, receive_link)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app = ApplicationBuilder().token("6914169408:AAF8iQV53vASbKiDHl7H2vRRLcDb85VhPqc").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(conversation_handler)

app.run_polling()

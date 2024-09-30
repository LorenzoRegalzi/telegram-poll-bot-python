import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import schedule
import time
import threading
import os
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

def send_poll(context: CallbackContext):
    question = "Quando se vedemo stronzi?"
    options = ["Lunedi (21:00-23:00)","Martedi (21:00-23:00)","Mercoledi (21:00-23:00)", "Giovedi (21:00-23:00)","Venerdi (21:00-23:00)", "Sabato (09:00-12:00)", "Domenica (09:00-12:00)", "Extra We Afternoon/Evening"]
    context.bot.send_poll(chat_id=GROUP_CHAT_ID, question=question, options=options, is_anonymous=False, allows_multiple_answers=True)

def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    update.message.reply_text(f"L'ID della chat è: {chat_id}")

def poll(update: Update, context: CallbackContext):
    send_poll(context) 
    

def schedule_poll():
    schedule.every().monday.at("10:00").do(send_poll, context=updater.job_queue)

    while True:
        schedule.run_pending()
        time.sleep(1)


updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('getid', get_chat_id))

threading.Thread(target=schedule_poll, daemon=True).start()

updater.start_polling()
updater.idle()

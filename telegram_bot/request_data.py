from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import pymysql
import os
from models import db

TOKEN: Final = os.environ["TOKEN"]
BOT_USERNAME: Final="@SwallowSpotBot"
INFO: Final= None

async def create_connection():

    mydb = pymysql.connect(
    host= os.getenv("SERVERNAME"),
    user= os.getenv("DBUSER"),
    password= os.getenv("PASSWORD"),
    database= os.getenv("DBNAME"),
    )
    return mydb

async def verify_user(chat_id):
    myresult = db.executeQueryOtherCursor(f"SELECT ID_telegram FROM Admin WHERE ID_telegram = {chat_id}")

    if myresult:
        return True
    else:
        return False

# Request database to find chat-id admin
async def find_id(INFO, chat_id):

    bot = Bot(token=TOKEN)

    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]

        myresult = db.executeQueryOtherCursor(f"SELECT ID_telegram FROM Admin WHERE ID_telegram = {chat_id}")

        for x in myresult:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=chat_id, text=x, reply_markup=reply_markup)
            print("Notifica inviata a "+x+" con successo!")

    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")

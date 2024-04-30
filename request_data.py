from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import mysql.connector
from read_pdf import create_connection
from main import CHAT_ID
TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 
INFO: Final= None

async def verify_user(chat_id):
    mydb = create_connection()
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT ID_telegram FROM Admin WHERE ID_telegram=={chat_id}")

    myresult = mycursor.fetchall()
    if(myresult==None):
        return False
    else:
        return True


#request database to find chat-id admin
async def snow_report():
    mydb = create_connection()
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]
        mycursor = mydb.cursor()

        mycursor.execute("SELECT path,MAX(date) FROM Snow_report")

        myresult = mycursor.fetchall()

        for x in myresult:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=CHAT_ID, text=x, reply_markup=reply_markup)
            print("Notifica inviata a "+x+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")

async def report():
    mydb = create_connection()
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]
        mycursor = mydb.cursor()

        mycursor.execute("SELECT path,MAX(date) FROM report")

        myresult = mycursor.fetchall()
        
        for x in myresult:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=CHAT_ID, text=x, reply_markup=reply_markup)
            print("Notifica inviata a "+x+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")

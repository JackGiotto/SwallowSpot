from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import pymysql
import json,os
import xmltodict
import urllib.request


TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 
INFO: Final= None







TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 


async def create_connection():

    mydb = pymysql.connect(
    host= os.getenv("SERVERNAME"),
    user= os.getenv("DBUSER"),
    password= os.getenv("PASSWORD"),
    database= os.getenv("DBNAME"),
    )
    return mydb    

async def verify_user(chat_id):
    mydb = await create_connection()
    
    mycursor = mydb.cursor()
    
    mycursor.execute(f"SELECT ID_telegram FROM Admin WHERE ID_telegram = {chat_id}")

    myresult = mycursor.fetchall()
       
    if myresult:
        return True
    else:
        return False


#request database to find chat-id admin
async def find_id(INFO,chat_id):
    
    mydb = create_connection()
    
    bot = Bot(token=TOKEN)
    
    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]
        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT ID_telegram FROM Admin WHERE ID_telegram = {chat_id}")



        myresult = mycursor.fetchall()
        for x in myresult:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=chat_id, text=x, reply_markup=reply_markup)
            print("Notifica inviata a "+x+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")




       
#check of the Barzizza XML by the Telegram bot when the alert is of the IDRO type
async def control():
    url = 'https://www.ambienteveneto.it/Dati/0283.xml'

    response = urllib.request.urlopen(url).read()

    # from XML to JSON
    data_dict = xmltodict.parse(response)
    json_data = json.dumps(data_dict, indent=4)
    data = json.loads(json_data)
    liv_idro = data["CONTENITORE"]["STAZIONE"]["SENSORE"][0]["DATI"]

    # Extract the latest value of "VM" (water level)
    val = liv_idro[-1]["VM"]
    
    print(val)

    liv = float(val)
    # control of the Brenta height value
    if liv >= 2.3 and liv < 2.8:
        return "GIALLO"
    elif liv >= 2.8 and liv < 3.2:
        return "ROSSO"
    elif liv >= 3.2:
        return "VIOLA"
    else:
        return "VERDE"            
    
from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import json
import xmltodict
import urllib.request
import mysql.connector


TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 


async def create_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="mydatabase"
    )
    return mydb    

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

        mycursor.execute("SELECT ID_telegram FROM Admin")

        myresult = mycursor.fetchall()

        for x in myresult:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=chat_id, text=x, reply_markup=reply_markup)
            print("Notifica inviata a "+x+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")



#invio in modo automoatico del bot ad un utente preciso
async def alert_control(tipo,colore,chat_id):
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]
       
        messaggio=" "
        if tipo =="hydraulic":
            colore= await control()
            if colore == "GIALLO":
                messaggio += "\nPericolo Giallo di idraulico"
            elif colore == "ROSSO":
                messaggio += "\nPericolo Rosso di idraulico"
            elif colore == "VIOLA":
                messaggio += "\nPericolo Rosso di idraulico"
            else: return
        elif tipo =="hydrogeological":        
            if colore  == "GIALLO":
                messaggio += "\nPericolo Giallo di idrogeologico"
            elif colore == "ROSSO":
                messaggio += "\nPericolo Rosso di idrogeologico"
        elif tipo =="storm":     
            if colore == "GIALLO":
                messaggio += "\nPericolo Giallo di Idrogeologica per Temporali"
            elif colore == "ROSSO":
                messaggio += "\nPericolo Rosso di Idrogeologica per Temporali"

        global INFO 
        INFO =  messaggio
        #find_id(messaggio)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await bot.send_message(chat_id=chat_id, text=messaggio, reply_markup=reply_markup)
        print("Notifica inviata a "+messaggio+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")

       
#controllo del XML di Barzizza da Parte del bot Telegram quando l'allerta è di tipo IDRO
async def control():
    url = 'https://www.ambienteveneto.it/Dati/0283.xml'

    # "prendo" l'XML dal Sito del Comune
    response = urllib.request.urlopen(url).read()

    # da XML a JSON
    data_dict = xmltodict.parse(response)
    json_data = json.dumps(data_dict, indent=4)
    data = json.loads(json_data)
    liv_idro = data["CONTENITORE"]["STAZIONE"]["SENSORE"][0]["DATI"]

    # Estrai l'ultimo valore di "VM" (livello idrometrico)
    val = liv_idro[-1]["VM"]
    
    print(val)

    liv = float(val)
    # controllo del valore dell'altezza del Brenta
    if liv >= 2.3 and liv < 2.8:
        return "GIALLO"
    elif liv >= 2.8 and liv < 3.2:
        return "ROSSO"
    elif liv >= 3.2:
        return "VIOLA"
    else:
        return "VERDE"            
    
#--------------------------------------------------------------------------------------------------
# function to verify snow alert value        
async def snow_control(update:Update, context,val,info,chat_id):
    bot = Bot(token=TOKEN)
    if(val==0):
        return
    else:
        try:
            keyboard = [
                [InlineKeyboardButton("Inoltra", callback_data='Send')],
                [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
            ]
            #find_id(messaggio)
            global INFO
            INFO="ALLERTA NEVE: "+info+" indice: "+val
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=chat_id, text=INFO, reply_markup=reply_markup)
            print("Notifica inviata a "+INFO+" con successo!")
        except TelegramError as e:
            print(f"Si è verificato un errore nell'invio della notifica: {e}")
    
        return
    

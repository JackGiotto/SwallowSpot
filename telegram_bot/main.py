from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import json
import requests
import xml.etree.ElementTree as ET
from telegram_bot.request_data import *
from models import db

#Credenziali per associare il Bot Telegram e il programma in python
TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 
CHAT_ID: Final = None
INDEX: Final=0
DATA: Final = {
    "idro":"",
    "idrogeo":"",
    "temp":""
}
DATASNOW: Final = None
INFO: Final= {
    "snow":["","",""],
    "idro":"",
    "idrogeo":"",
    "temp":""
}
        
#function start when admin use the command "/start"
async def start_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    global CHAT_ID
    chat_id = update.message.chat_id
    CHAT_ID = chat_id
    #function to check if the user who is using the bot is admin
    control=await verify_user(chat_id)
    if(control==False):
        #button to send chat_id to admin to link the account telegram with site account
        keyboard = [
            [InlineKeyboardButton("Dimmi il mio Chat ID ", callback_data='chat_id')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"⛔ Il tuo account Telegram non ha i privilegi per usare questo Bot ⛔",reply_markup=reply_markup)
    
    else:    
        #button to do a manual control of last bulletin uploaded in database 
        keyboard = [
            [InlineKeyboardButton("⛄ Bol. PREVISIONE LOCALE NEVICATE ⛄ ", callback_data='Neve')],
            [InlineKeyboardButton("🌧️ Bol. IDROGEOLOGICA ED IDRAULICA 🌧️", callback_data='Idro')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"☀️ ciao sono il tuo bot per vedere le allerte meteo della Zona di Bassano Del Grappa ☀️",reply_markup=reply_markup)
    

#invio in modo automoatico del bot ad un utente preciso
async def alert_control(tipo, colore):
    bot = Bot(token=TOKEN)
    global INFO
    import requests

  
    keyboard = []  # Definisci e inizializza la variabile keyboard

    query = """
                SELECT GroupID as chat_id
                FROM Admin;
            """
    result = db.executeQueryOtherCursor(query)
    try:
        messaggio = ""  # Assicurati che il messaggio non sia vuoto
        if tipo == "idraulico":
            print("CHAT ID", result)
            print("colore",str(colore))
            if colore == "GIALLA":
                messaggio = "\nPericolo Giallo di idraulico 🟡"
            elif colore == "ARANCIONE":
                messaggio = "\nPericolo Arancione di idraulico 🟠"    
            elif colore == "ROSSA":
                messaggio = "\nPericolo Rosso di idraulico 🔴"
            elif colore == "VIOLA":
                messaggio = "\nPericolo Viola di idraulico 🟣"    
            else: 
                return;    
            INFO["idro"] = messaggio
            tmp = 'sendidro'
        elif tipo == "idrogeologico":
            if colore == "GIALLA":
                messaggio = "\nPericolo Giallo di idrogeologico 🟡"
            elif colore == "ARANCIONE":
                messaggio = "\nPericolo Arancione di idrogeologico 🟠"    
            elif colore == "ROSSO":
                messaggio = "\nPericolo Rosso di idrogeologico 🔴"
            INFO["idrogeo"] = messaggio
            tmp = 'sendidrogeo'
        elif tipo == "idrogeologico con temporali":
            if colore == "GIALLA":
                messaggio = "\nPericolo Giallo di Idrogeologica per Temporali 🟡"
            elif colore == "ARANCIONE":
                messaggio = "\nPericolo Arancione di idrogeologico  per Temporali 🟠"   
            elif colore == "ROSSO":
                messaggio = "\nPericolo Rosso di Idrogeologica per Temporali 🔴"
            INFO["temp"] = messaggio
            tmp = 'sendtem'
        else: 
            return    
        # Assicurati che il messaggio non sia vuoto prima di inviarlo
        
        if messaggio:
            keyboard = [
                [InlineKeyboardButton("Inoltra", callback_data=tmp)],
                [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            for x in result:
                t_id=x[0]
                params = {
                    'chat_id': t_id,
                    'text': messaggio,
                    'reply_markup': reply_markup.to_json()  # Converte la tastiera inline in JSON
                }

                # Effettua la richiesta POST per inviare il messaggio
                response = requests.post(url, json=params)

                #await bot.send_message(chat_id=int(t_id), text=messaggio, reply_markup=reply_markup)
                print("Notifica inviata a " + messaggio + " con successo!")
        else:
            print("Il messaggio è vuoto, non inviato.")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")


async def snow_control(val):
    bot = Bot(token=TOKEN)
    global INDEX
    index=0  
    query = """
                SELECT GroupID as chat_id
                FROM Admin;
            """
    result = db.executeQueryOtherCursor(query)

    for giorno in val:
        index=index+1
        if giorno['1000 m'] != "0":
            
            try:
                if index==1:
                    keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendsnow1')],
                        [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
                    ]
                elif  index==2: 
                     keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendsnow2')],
                        [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
                    ] 
                elif  index==3: 
                     keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendsnow3')],
                        [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
                    ]      
                #find_id(messaggio)
                global INFO
                messaggio=" 🌨️ALLERTA NEVE🌨️ \n Livello: "+giorno['1000 m']+" \n Data:"+giorno['date']
                # Aggiungi il messaggio allerta neve alla lista
                if(INDEX<=3):
                    INDEX += 1
                else:
                    INDEX=0
                INFO["snow"][INDEX]=(messaggio)    
                print("mess:"+INFO["snow"][INDEX])
                reply_markup = InlineKeyboardMarkup(keyboard)
                for x in result:
                    t_id=x[0]
                    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
                    params = {
                        'chat_id': t_id,
                        'text': INFO["snow"][INDEX],
                        'reply_markup': reply_markup.to_json()  # Converte la tastiera inline in JSON
                    }

                    # Effettua la richiesta POST per inviare il messaggio
                    response = requests.post(url, json=params)
                    
            except TelegramError as e:
                print(f"Si è verificato un errore nell'invio della notifica: {e}")
        
            
        
    return "Dati non disponibili per il primo giorno"

#function to associate the buttons and functions of the bot  
async def button(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()
    data = query.data
    if data == 'Neve':
        await snow_report()
    elif data == 'Idro':
        await report() 
    elif data == 'sendi':
        await manual_send(update, context,"idro")
    elif data == 'sendig':            
        await manual_send(update, context,"idrogeo")  
    elif data == 'sendt':
        await manual_send(update, context,"temp")               
    elif data == 'sendidro':
        await send(update, context,"idro", None)  
    elif data == 'sendidrogeo':
        await send(update, context,"idrogeo",None)
    elif data == 'sendtem':
        await send(update, context,"temp",None)
    elif data == 'sendsnow1':
        await send(update, context,"snow",1)
    elif data == 'sendsnow2':
        await send(update, context,"snow",2)
    elif data == 'sendsnow3':
        await send(update, context,"snow",3)        
    elif data == 'Drop':
        await drop(update, context)
    elif data == 'chat_id':
        await give_id(update,chat_id)
  
#request database to find chat-id admin 
async def give_id(update: Update,chat_id_value):
    query = update.callback_query
    bot = Bot(token=TOKEN)
    await query.edit_message_text(text=f"ecco il tuo chat id")
    await bot.send_message(chat_id=chat_id_value, text=f"{chat_id_value}")

#function to forward the alert of the message sent to the admin to the Telegram group
async def send(update:Update, context,arg,index):
    global INFO
    bot = Bot(token=TOKEN)
    query = update.callback_query
    await query.answer()
    print(INFO[arg])
    try:
        with open("./data.json", "r") as doc:
            data = json.load(doc)
            id = data["GROUP_ID"]
            print(INFO[arg])
            if(index==None):
                await bot.send_message(chat_id=id, text=INFO[arg])
            else: 
                await bot.send_message(chat_id=id, text=INFO[arg][index])    
                
        await query.edit_message_text(text="Notifica inviata con successo!")
    except FileNotFoundError:
        print("File JSON non trovato.")
        await query.edit_message_text(text="File JSON non trovato.")
    except KeyError:
        print("Chiave GROUP_ID non presente nel file JSON.")
        await query.edit_message_text(text="Chiave GROUP_ID non presente nel file JSON.")        
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")
        await query.edit_message_text(text=f"Si è verificato un errore nell'invio della notifica: {e}")
    

#function to not forward the alert of the message sent to the admin to the Telegram group
async def drop(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Hai rifiutato l'inoltro di questa allerta")
    
#function for printing the type of error in the event of an error on the terminal
async def error(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    print(f'Update {update} causato da {context.error}')

#function to download the last bulletin uploaded in database to do a manual control
async def report():
    #mydb = await create_connection()
    global DATA
    bot = Bot(token=TOKEN)
    try:
        #mycursor = mydb.cursor()
        
        #query to select last info of VENE-B
        query = (
            "SELECT Criticalness.ID_color, Criticalness.ID_risk, Color.color_name "
            "FROM Area "
            "JOIN Criticalness ON Area.ID_area = Criticalness.ID_area "
            "JOIN Color ON Criticalness.ID_color = Color.ID_color "
            "JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk "
            "WHERE Area.area_name = 'Vene-B' and Risk.ID_risk!='4'"
            "ORDER BY Criticalness.ID_issue DESC "
            "LIMIT 3"
        )
        #mycursor.execute(query)
        myresult = db.executeQueryOtherCursor(query)
        print(myresult)

        #control the type and alertness of the data taken from the query
        for x in myresult:
            print(x)
            if x[0]==1:
                messaggio="nessun pericolo 🟢";
                await bot.send_message(chat_id=CHAT_ID, text=messaggio)
            else:
                if(x[1]==1):
                    keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendi')],
                        [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
                    ]
                    messaggio=f"Allerta grado: {x[2]} tipo: idraulico 🌧️"
                    DATA["idro"]=messaggio
                elif(x[1]==2):
                    keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendig')],
                        [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
                    ]
                    messaggio=f"Allerta grado: {x[2]} tipo: idrogeologico 🌧️"
                    DATA["idrogeo"]=messaggio
                elif(x[1]==3):
                    keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendt')],
                        [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
                    ]
                    messaggio=f"Allerta grado: {x[2]} tipo: idrogeologico con temporali ⛈️"
                    DATA["temp"]=messaggio        
                    print(x[1])
                reply_markup = InlineKeyboardMarkup(keyboard)
                await bot.send_message(chat_id=CHAT_ID, text=messaggio, reply_markup=reply_markup)
            print("Notifica inviata a "+str(CHAT_ID)+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")

#function to download the last bulletin uploaded in database to do a manual control
async def snow_report():
    #mydb = await create_connection()
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]
        #mycursor = mydb.cursor()

        query = """
            SELECT Snow_criticalness_altitude.value, Snow_criticalness.date
            FROM Area 
            JOIN Snow_criticalness ON Area.ID_area = Snow_criticalness.ID_area 
            JOIN Snow_criticalness_altitude ON Snow_criticalness_altitude.ID_snow_issue = Snow_criticalness.ID_snow_issue
            JOIN Altitude ON Snow_criticalness_altitude.ID_altitude = Altitude.ID_altitude
            WHERE Area.area_name = 'Altopiano dei sette comuni' and Altitude.height= '1000 m'
            ORDER BY Snow_criticalness.ID_snow_issue DESC
            LIMIT 3;
        """
        myresult = db.executeQueryOtherCursor(query)
        global DATASNOW
        if not myresult:
            await bot.send_message(chat_id=CHAT_ID, text="Dato Non Disponibile")
        for x in myresult:
            if x[0]==0:
                await bot.send_message(chat_id=CHAT_ID, text="nessun pericolo 🟢")
            else:
                if(x[1]==4):
                    messaggio=f"Allerta neve 🌨️, livello{x[0]}"
                    DATASNOW = messaggio
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await bot.send_message(chat_id=CHAT_ID, text=messaggio, reply_markup=reply_markup)    
                    
            print("Notifica inviata a "+str(CHAT_ID)+" con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")
    
   
#function to forward the alert of the message sent to the admin to the Telegram group
async def manual_send(update:Update, context,arg):
    global DATA
    bot = Bot(token=TOKEN)
    query = update.callback_query
    await query.answer()
    
    try:
        with open("./data.json", "r") as doc:
            data = json.load(doc)
            id = data["GROUP_ID"]
            await bot.send_message(chat_id=id, text=DATA[arg])    
                
        await query.edit_message_text(text="Notifica inviata con successo!")
    except FileNotFoundError:
        print("File JSON non trovato.")
        await query.edit_message_text(text="File JSON non trovato.")
    except KeyError:
        print("Chiave GROUP_ID non presente nel file JSON.")
        await query.edit_message_text(text="Chiave GROUP_ID non presente nel file JSON.")        
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")
        await query.edit_message_text(text=f"Si è verificato un errore nell'invio della notifica: {e}")

async def manual_send_snow(update:Update, context):
    global DATASNOW
    bot = Bot(token=TOKEN)
    query = update.callback_query
    await query.answer()
    
    try:
        with open("./data.json", "r") as doc:
            data = json.load(doc)
            id = data["GROUP_ID"]
            await bot.send_message(chat_id=id, text=DATASNOW)    
                
        await query.edit_message_text(text="Notifica inviata con successo!")
    except FileNotFoundError:
        print("File JSON non trovato.")
        await query.edit_message_text(text="File JSON non trovato.")
    except KeyError:
        print("Chiave GROUP_ID non presente nel file JSON.")
        await query.edit_message_text(text="Chiave GROUP_ID non presente nel file JSON.")        
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")
        await query.edit_message_text(text=f"Si è verificato un errore nell'invio della notifica: {e}")
 
async def get_group_id(update: Update, context):
    # Ottieni l'ID del gruppo
    group_id = update.message.chat_id
    
    # Invia l'ID del gruppo come risposta al comando
    await update.message.reply_text(f"L'ID di questo gruppo è: {group_id}")
            
def start_bot():
    app = Application.builder().token(TOKEN).build()
        
    #associazione ai comandi del bot alle funzione
    app.add_handler(CommandHandler('start', start_command))
    #app.add_handler(CommandHandler('help', help_command))
    #app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler("get_group_id", get_group_id))
    app.add_handler(CallbackQueryHandler(button))
    
    
    app.add_error_handler(error)
    print("Polling....")
    app.run_polling(poll_interval=3)


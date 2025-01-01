from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler,CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import json
import requests
from telegram_bot.request_data import *
from models import db

#Credenziali per associare il Bot Telegram e il programma in python
TOKEN = ""
BOT_USERNAME: Final="@SwallowSpotBot"
CHAT_ID: Final = None
INDEX: Final=0
DATA: Final = {
    "idro":"",
    "idrogeo":"",
    "temp":""
}
waiting_for_message = {}
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
            [InlineKeyboardButton("🌧️ Bol. IDROGEOLOGICA ED IDRAULICA 🌧️", callback_data='Idro')],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"☀️ ciao sono il tuo bot per vedere le allerte meteo della Zona di Bassano Del Grappa ☀️",reply_markup=reply_markup)


#send message a single user
async def alert_control(tipo, colore):
    bot = Bot(token=TOKEN)
    global INFO
    import requests

  
    keyboard = [] 

    query = """
                SELECT GroupID as chat_id
                FROM Admin;
            """
    result = db.executeQueryOtherCursor(query)
    try:
        messaggio = "" 
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
                [InlineKeyboardButton("Modifica messaggio", callback_data='wait')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            for x in result:
                t_id=x[0]
                params = {
                    'chat_id': t_id,
                    'text': messaggio,
                    'reply_markup': reply_markup.to_json()
                }

                # do POST request to send message
                response = requests.post(url, json=pardispatcherams)

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
                    ]
                elif  index==2:
                     keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendsnow2')],
                    ] 
                elif  index==3: 
                     keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendsnow3')],
                    ]
                keyboard.append([InlineKeyboardButton("Rifiuta", callback_data='Drop')])
                keyboard.append([InlineKeyboardButton("Modifica messaggio", callback_data='wait')])      
                       
                global INFO
                messaggio=" 🌨️ALLERTA NEVE🌨️ \n Livello: "+giorno['1000 m']+" \n Data:"+giorno['date']
                # add message snow allert in list
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
                        'reply_markup': reply_markup.to_json()  
                    }

                    # Post request to send message
                    response = requests.post(url, json=params)

            except TelegramError as e:
                print(f"Si è verificato un errore nell'invio della notifica: {e}")



    return "Dati non disponibili per il primo giorno"

async def ins(chat_id):
    dati = [
        {
            "date": "18-01-2024 00:00:00",
            "%": "0",
            "1000 m": "2",
            "1500 m": "0",
            ">1500 m": "0"
        },
        {
            "date": "19-01-2024 00:00:00",
            "%": "0",
            "1000 m": "0",
            "1500 m": "0",
            ">1500 m": "0"
        },
        {
            "date": "20-01-2024 00:00:00",
            "%": "0",
            "1000 m": "0",
            "1500 m": "0",
            ">1500 m": "0"
        }
    ]

    
    await snow_control(dati,chat_id)

    data={
        "hydraulic": "ROSSO",
        "hydrogeological": "GIALLO",
        "storm": "GIALLO"
    }
    for tipo, colore in data.items():
        if(colore!="VERDE"):
            await alert_control(tipo,colore,chat_id)


#function to associate the buttons and functions of the bot  
async def button(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    bot = Bot(token=TOKEN)
    await query.answer()
    data = query.data
    if data == 'wait':
            
        # update message to remove buttons
        await bot.send_message(chat_id=chat_id, text="Ok, sto aspettando il tuo messaggio.")
        waiting_for_message[user_id] = True

    elif data == 'Neve':
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
    global DATA
    bot = Bot(token=TOKEN)
    try:        
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
                    ]
                    messaggio=f"Allerta grado: {x[2]} tipo: idraulico 🌧️"
                    DATA["idro"]=messaggio
                elif(x[1]==2):
                    keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendig')],
                    ]
                    messaggio=f"Allerta grado: {x[2]} tipo: idrogeologico 🌧️"
                    DATA["idrogeo"]=messaggio
                elif(x[1]==3):
                    keyboard = [
                        [InlineKeyboardButton("Inoltra", callback_data='sendt')],
                    ]
                keyboard.append([InlineKeyboardButton("Rifiuta", callback_data='Drop')])
                keyboard.append([InlineKeyboardButton("Modifica messaggio", callback_data='wait')])      
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
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
            [InlineKeyboardButton("Inoltra", callback_data='Send')],
            [InlineKeyboardButton("Rifiuta", callback_data='Drop')],
        ]

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
                    messaggio=f"Allerta neve 🌨️, altezza: {x[0]} cm"
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
    # Get Group ID
    group_id = update.message.chat_id
    
    # Send GroupID
    await update.message.reply_text(f"L'ID di questo gruppo è: {group_id}")
            
async def handle_message(update: Update, context: CallbackContext):
    bot = Bot(token=TOKEN)
    query = update.callback_query
    user_id = update.message.from_user.id
    if waiting_for_message.get(user_id):
        user_message = update.message.text
        await update.message.reply_text(f'messaggio inviato: {user_message}')
        with open("./data.json", "r") as doc:
            data = json.load(doc)
            id = data["GROUP_ID"]
                
            await bot.send_message(chat_id=id, text=user_message)                
        # Stop Waiting status of user
        waiting_for_message[user_id] = False
    else:
        await update.message.send_message('Non sto aspettando un messaggio da te.')

def start_bot(token: str):
    global TOKEN
    TOKEN = token

    app = Application.builder().token(TOKEN).build()

    #association of bot commands with functions
    app.add_handler(CommandHandler('start', start_command))
   
    app.add_handler(CommandHandler("get_group_id", get_group_id))
    app.add_handler(CallbackQueryHandler(button))
    
    
    app.add_error_handler(error)
    print("Polling....")
    app.run_polling(poll_interval=3)


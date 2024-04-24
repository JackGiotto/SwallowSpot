from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import json
import xml.etree.ElementTree as ET
from read_pdf import *
from request_data import *

#Credenziali per associare il Bot Telegram e il programma in python
TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 
CHAT_ID: Final = None
INFO: Final= None



        
# le funzioni che partano in base al comando inviato al bot Telegram
async def start_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    global CHAT_ID  # Indica che si sta facendo riferimento alla variabile globale CHAT_ID
    chat_id = update.message.chat_id
    CHAT_ID = chat_id
    
    
    data={
        "hydraulic": "ROSSO",
        "hydrogeological": "GIALLO",
        "storm": "GIALLO"
    }
    for tipo, colore in data.items():
        if(colore!="VERDE"):
            await alert_control(tipo,colore)
        
    keyboard = [
        [InlineKeyboardButton("Bol. PREVISIONE LOCALE NEVICATE ", callback_data='Neve')]
        [InlineKeyboardButton("Bol. IDROGEOLOGICA ED IDRAULICA", callback_data='Idro')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f" ciao sono il tuo bot per vedere se il mondo sta finendo figlio di troia questo è il tuo id {chat_id}",reply_markup=reply_markup)
   
  
#funzione per associare i bottoni e le funzioni del bot        
async def button(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()
    data = query.data
    if data == 'Neve':
        await snow_report()
    elif data == 'Idro':
        await report()
    elif data == 'Send':
        await send(update, context, INFO)
    elif data == 'Drop':
        await drop(update, context)

    #elif data == 'opzione3':
       # da cambiare per capire come fa re        
 

# Funzione per gestire l'opzione 1 del bottone
async def send(update:Update, context,info):
    bot = Bot(token=TOKEN)
    query = update.callback_query
    await query.answer()
    try:
        with open("./data.json", "r") as doc:
            data = json.load(doc)
            id = data["GROUP_ID"]
            await bot.send_message(chat_id=id, text=info)
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
    

# Funzione per gestire l'opzione 2 del bottone
async def drop(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Hai rifiutato l'inoltro di questa allerta")
    

#funzione per l'invio del messaggio in base al msg dell'utente
def handle_response(update:Update,text: str)-> str:
    processed: str=text.lower()
    if'ciao' in processed:
        return 'ciao'
    if 'gg' in processed:
        chat_id = update.message.chat_id
        return f'ok ti mostro il vostro chatid {chat_id}'
    return 'errore'


#funzione per interagiore con il bot da un gruppo Telegram
async def handle_message(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    message_type : str = update.message.chat.type
    text : str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str=handle_response(update,new_text)
        else:
            return
    else:
        response: str=handle_message(text)
    
    print('Bot:',response)
    
    await update.message.reply_text(response)


async def error(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    print(f'Update {update} causato da {context.error}')
    
if __name__=='__main__':
    app = Application.builder().token(TOKEN).build()

    
    #associazione ai comandi del bot alle funzione
    app.add_handler(CommandHandler('start', start_command))
 #   app.add_handler(CommandHandler('help', help_command))
  #  app.add_handler(CommandHandler('custom', custom_command))
    
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    
    
    app.add_error_handler(error)
    print("Polling....")
    app.run_polling(poll_interval=3)
    
    
from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
import json
import xmltodict
import xml.etree.ElementTree as ET
import urllib.request

TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 
CHAT_ID: Final = None

async def start_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    global CHAT_ID  # Indica che si sta facendo riferimento alla variabile globale CHAT_ID
    chat_id = update.message.chat_id
    CHAT_ID = chat_id
    keyboard = [
        [InlineKeyboardButton("Controlla", callback_data='opzione3')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f" ciao sono il tuo bot per vedere se il mondo sta finendo figlio di troia questo è il tuo id {chat_id}",reply_markup=reply_markup)
   
    
async def help_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text(" ciao sono il tuo bot per vedere se il mondo sta finendo in cosa ti devo aiutare")
    

async def custom_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text("Personalizzami")

async def invia_notifica(messaggio):
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
        [InlineKeyboardButton("Accetta", callback_data='opzione1')],
        [InlineKeyboardButton("Rifiuta", callback_data='opzione2')],
        [InlineKeyboardButton("Controlla", callback_data='opzione3')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await bot.send_message(chat_id=CHAT_ID, text=messaggio,reply_markup=reply_markup)  # Attendere il completamento della coroutine
        print("Notifica inviata con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")


async def control(update: Update, context):
    
    url = 'https://www.ambienteveneto.it/Dati/0283.xml'
    response = urllib.request.urlopen(url).read()
    data_dict = xmltodict.parse(response)
    json_data = json.dumps(data_dict,indent=4)
    data=json.loads(json_data)
    liv_idro=data["CONTENITORE"]["STAZIONE"]["SENSORE"][0]["DATI"]
    # Estrai l'ultimo valore di "VM" (livello idrometrico)
    print(liv_idro[-1]["VM"])
    #ultimo_valore_VM = livelli_idrometrici[-1]["VM"]
    val=liv_idro[-1]["VM"]
    liv=float(val)
    if(liv>=2.3):
        response="AO ZI ER BRENTA STA AL PRIMO LIVELLO STA AD ALTEZZA",val
        response = ' '.join(response)
        await invia_notifica(response)
    elif(liv>=2.8):
        response="AO ZI ER BRENTA STA AL PRIMO LIVELLO STA AD ALTEZZA",val
        response = ' '.join(response)
        await invia_notifica(response)
    elif(liv>=3.2):
        response="AO ZI ER BRENTA STAMO A GIOCA A CARTE CON I PESCI TIE BECCATE STA ALTEZZA",val
        response = ' '.join(response)
        await invia_notifica(response)
    else:
        response="STIAMO NER BING CHILLING STIAMO AD ALTEZZA",val
        response = ' '.join(response)
        await invia_notifica(response)   
        
async def button(update: Update, context):
    query = update.callback_query
    chat_id = update.message.chat_id
    await query.answer()
    data = query.data
    if data == 'opzione1':
        await send(update, context)
    elif data == 'opzione2':
        await delete(update, context)
    elif data == 'opzione3':
        await control(update, context,chat_id)

# Funzione per gestire l'opzione 1
async def send(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="cx")

# Funzione per gestire l'opzione 2
async def delete(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Hai selezionato l'opzione 2")
    
#Risposte

def handle_response(text: str)-> str:
    processed: str=text.lower()
    if'ciao' in processed:
        return 'ciao'
    if 'mostramelo' in processed:
        chat_id = Update.message.chat_id
        return f'ok ti mostro il vostro chatid {chat_id}'
    return 'errore'

async def handle_message(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    message_type : str = update.message.chat.type
    text : str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str=handle_response(new_text)
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

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    
    app.add_error_handler(error)
    print("Polling....")
    app.run_polling(poll_interval=3)
    
    
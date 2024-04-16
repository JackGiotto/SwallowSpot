from typing import Final
from telegram import Update ,Bot
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes ,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError


TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 
CHAT_ID: Final = "741878550"

async def start_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    chat_id = update.message.chat_id
    await update.message.reply_text(f" ciao sono il tuo bot per vedere se il mondo sta finendo figlio di troia questo è il tuo id {chat_id}")
    await invia_notifica(f"CIAO")


async def help_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text(" ciao sono il tuo bot per vedere se il mondo sta finendo in cosa ti devo aiutare")
    
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == 'opzione1':
        await opzione1_function(update, context)
    elif data == 'opzione2':
        await opzione2_function(update, context)

# Funzione per gestire l'opzione 1
async def opzione1_function(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Hai selezionato l'opzione 1")

# Funzione per gestire l'opzione 2
async def opzione2_function(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Hai selezionato l'opzione 2")
    

async def custom_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text("Personalizzami")

async def invia_notifica(messaggio):
    bot = Bot(token=TOKEN)
    try:
        keyboard = [
        [InlineKeyboardButton("Opzione 1", callback_data='opzione1')],
        [InlineKeyboardButton("Opzione 2", callback_data='opzione2')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await bot.send_message(chat_id=CHAT_ID, text=messaggio,reply_markup=reply_markup)  # Attendere il completamento della coroutine
        print("Notifica inviata con successo!")
    except TelegramError as e:
        print(f"Si è verificato un errore nell'invio della notifica: {e}")

#Risposte

def handle_response(text: str)-> str:
    processed: str=text.lower()
    if'ciao' in processed:
        return 'ciao'
    if 'ti amo' in processed:
        return 'anch\'io <3 kiss kiss'
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
    
    
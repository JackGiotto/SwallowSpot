from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler,filters , ContextTypes


TOKEN: Final = "6557124632:AAEDrrKgTkiVbmmQFQdKZAiyVG3woS5j-oE"
BOT_USERNAME: Final="@SwallowSpotBot" 


async def start_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text(" ciao sono il tuo bot per vedere se il mondo sta finendo")
    


async def help_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text(" ciao sono il tuo bot per vedere se il mondo sta finendo in cosa ti devo aiutare")
    
    

async def custom_command(update:Update , context:ContextTypes.DEFAULT_TYPE ):
    await update.message.reply_text("Personalizzami")

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
    
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    
    app.add_error_handler(error)
    
    print("Polling....")
    app.run_polling(poll_interval=3)
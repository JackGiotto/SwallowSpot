from utils.cfd_analyzer.pdf_reader import Pdf_reader
from telegram_bot.main import start_bot, snow_control, alert_control
from threading import Thread
import asyncio

async def tuamamma():
    await alert_control(tipo, colore)

def saluta():
    p = Pdf_reader("./bulletins/test2.pdf")
    
    for tipo, colore in p.get_cfd_data()["risks"]["Vene-B"]["risks_value"].items():
        print(tipo, colore)
        if (colore != "VERDE"):
            tuamamma()

t = Thread(target=saluta)
t.start() 

start_bot()




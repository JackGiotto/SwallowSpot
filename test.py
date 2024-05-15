from utils.cfd_analyzer.pdf_reader import Pdf_reader
from telegram_bot.main import start_bot, snow_control, alert_control
from threading import Thread
import asyncio
from mail.mail import start_cycle

async def saluta():
    p = Pdf_reader("./bulletins/prova.txt")
    
    for tipo, colore in p.get_cfd_data()["risks"]["Vene-B"]["risks_value"].items():
        print(tipo, colore)
        if colore != "VERDE":
            await alert_control(tipo, colore)
    
    p = Pdf_reader("./bulletins/test_snow.txt")
    
    p.get_cfd_data()["risks"]["Altopiano dei sette comuni"]
    await snow_control(p.get_cfd_data()["risks"]["Altopiano dei sette comuni"])        

def run_saluta():
    asyncio.run(saluta())



t = Thread(target=start_cycle, name="emails")
t.start()
start_bot()
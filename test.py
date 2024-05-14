from utils.cfd_analyzer.pdf_reader import Pdf_reader
from telegram_bot.main import start_bot, alert_control,snow_control
from threading import Thread
from utils.db_backup.client_backup import start_backup
import asyncio

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

def main():
    t = Thread(target=run_saluta)
    t.start()
    start_bot()

# Run the main function
#main()
start_backup("192.168.0.12", "8495")

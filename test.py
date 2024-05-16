from utils.cfd_analyzer.pdf_reader import Pdf_reader
from telegram_bot.main import start_bot, snow_control, alert_control
from threading import Thread
import asyncio
from mail.mail import start_cycle
from time import sleep

async def saluta():
    await alert_control("idraulico", "GIALLA")       

def run_saluta():
    asyncio.run(saluta())



t = Thread(target=run_saluta, name="emails")
t.start()
start_bot()


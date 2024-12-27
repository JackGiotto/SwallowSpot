from telegram_bot.main import start_bot
from threading import Thread
from mail.mail import start_cycle
import os
from dotenv import load_dotenv


load_dotenv()
start_path = "./"
os.environ["start_path"] = start_path

t = Thread(target=start_cycle, name="emails")
t.start()

start_bot()

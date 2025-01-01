from telegram_bot.main import start_bot
from threading import Thread
from mail.mail import start_cycle
import os
from dotenv import load_dotenv
from utils.wsgi_utils import read_env_file



if __name__ == "__main__":
    load_dotenv()
    start_path = "./"
else:
    start_path = "/var/www/swallowspot.it/SwallowSpot/"
    read_env_file(start_path + ".env")

os.environ["start_path"] = start_path

t = Thread(target=start_cycle, name="emails")
t.start()

start_bot()

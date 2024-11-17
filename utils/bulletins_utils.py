from utils.cfd_analyzer.pdf_reader import Pdf_reader
from werkzeug.utils import secure_filename
import os
import PyPDF2
from telegram_bot.main import alert_control, snow_control
import asyncio

def save_bulletin(file, filename = None) -> str:
    """saves bulletin in bulletins folder and in the database

    Args:
        file (pdf, bytes): PDF object or bytes from email
        filename (str, optional): Name of the file, not needed for PDF object. Defaults to None.

    Returns:
        str: error or success tring
    """
    if isinstance(file, bytes):
        file_bytes = file
        email = True
    else:
        # Assume the input is a file object
        filename = secure_filename(file.filename)
        file_bytes = file.read()
        email = False
    
    if filename.endswith('.pdf'):
        filename = _unique_filename(os.getenv("BULLETINS_FOLDER"), filename)
        file_path = os.path.join(os.getenv("BULLETINS_FOLDER"), filename)
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
        
        pdf_class = _get_bulletin_class(file_path)
        if pdf_class != None:
            try:
                pdf_class.add_to_db()
                if email:
                    if pdf_class.type == "hydro":
                        asyncio.run(_hydro_telegram(pdf_class.get_cfd_data()))
                    else:
                        asyncio.run(_snow_telegram(pdf_class.get_cfd_data()))
                os.remove(file_path)
            except Exception as e:
                # database error (the report is already added)
                print(e)
                os.remove(file_path)
                return "Errore: errore durante l'inserimento nel database, il bollettino potrebbe essere già stato inserito"
            return 'Success'
        else:
            # the file is a pdf but does not follow CFD bulletins standards
            os.remove(file_path)
            return 'Errore: Il file caricato non non è nel formato giusto'
    else:
        # the file is not a pdf
        return 'Errore: il file caricato non è un PDF'

def _get_bulletin_class(path) -> Pdf_reader:
    """get the PDF reader class for the given path

    Args:
        path (str): file path

    Returns:
        PDF_reader: pdf reader class or None
    """
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            if reader.numPages > 0:
                bulletin_class = Pdf_reader(path)
                if (bulletin_class.analyzer == None):
                    print("errore in bulletin")
                    return None
                else:
                    return bulletin_class
            else:
                return None
    except:
        print("errore")
        return None

def _unique_filename(directory, filename) -> str:
    """checks if the filename is unique, if not it add a number in the end

    Args:
        directory (str): directory path
        filename (str): name of the file

    Returns:
        str: unique filename
    """

    counter = 1
    base, ext = os.path.splitext(filename)
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


async def _hydro_telegram(data):
    # send message to admins
    for tipo, colore in data["risks"]["Vene-B"]["risks_value"].items():
        print(tipo, colore)
        if colore != "VERDE":
            await alert_control(tipo, colore)

async def _snow_telegram(data):
    # send message to admins
    await snow_control(data["risks"]["Altopiano dei sette comuni"])
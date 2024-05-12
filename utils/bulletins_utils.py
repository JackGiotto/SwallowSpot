from utils.cfd_analyzer.pdf_reader import Pdf_reader
from werkzeug.utils import secure_filename
import os
import PyPDF2

def save_bulletin(file) -> str:
    if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filename = _unique_filename(os.getenv("BULLETINS_FOLDER"), filename)
            file_path = os.path.join(os.getenv("BULLETINS_FOLDER"), filename)
            file.save(file_path)
            

            pdf_class = _get_bulletin_class(file_path)
            if pdf_class != None:
                try:
                    pdf_class.add_to_db()
                except Exception as e:
                    print(e)
                    os.remove(file_path)
                    return "Errore: errore durante l'inserimento nel database, il bollettino potrebbe essere già stato inserito"
                return 'Success'
            else:
                os.remove(file_path)
                return 'Errore: Il file caricato non non è nel formato giusto'
    else:
        return 'Errore: il file caricato non è un PDF'

def _get_bulletin_class(path):
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

def _unique_filename(directory, filename):
    counter = 1
    base, ext = os.path.splitext(filename)
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename
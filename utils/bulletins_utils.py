from utils.cfd_analyzer.pdf_reader import Pdf_reader
from werkzeug.utils import secure_filename
import os
import PyPDF2

def save_bulletin(file) -> str:
    if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(os.getenv("BULLETINS_FOLDER"), filename)
            file.save(file_path)
            

            pdf_class = _get_bulletin_class(file_path)
            if pdf_class != None:
                return 'File is a PDF and has been uploaded successfully.'
            else:
                os.remove(file_path)
                return '-1 File is not a PDF or cannot be read.'
    else:
        return 'File is not a PDF'

def _get_bulletin_class(path):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            if reader.numPages > 0:
                bulletin_class = Pdf_reader(path)
                if (bulletin_class.analyzer == None):
                    return None
                else:
                    return bulletin_class
            else:
                return None
    except PyPDF2.utils.PdfReadError:
        return None
import os
import shutil
import tempfile
from subprocess import check_call
import PyPDF2 as p2
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO

from setup_logger import SetupLogger


class TranscriptParser:
    def __init__(self, filename, file_data):
        self.file_data = file_data
        self.filename = filename
        self.parser_logger = SetupLogger('transcript_parser.log', True)

    def get_name(self):
        pass

    def get_student_id(self):
        pass

    def read_pdf(self):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams(char_margin=200)
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # fp = open(self.filename, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        
        for page in PDFPage.get_pages(self.file_data, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=False):
            interpreter.process_page(page)
       
        textstr = retstr.getvalue()

        # fp.close()
        device.close()
        retstr.close()
        return textstr

    def parse1(self):
        file_string = self.read_pdf()
        print(file_string)
        with open("delete1.txt", "a") as f:
            f.write(file_string)

    def parse(self):
        pdf_binary = open(self.filename, 'rb')
        pdf_reader = p2.PdfFileReader(pdf_binary)

        if pdf_reader.isEncrypted:
            '''
            pyPDF2 requires the pdf be decrypted.
            <Encryption Level: 128-bit AES> raises NotImplementedError
            <Encryption level: 128-bit RC4> can be decrypted with empty string
            '''
            try:
                pdf_reader.decrypt('')
                self.parser_logger.info('File Decrypted (PyPDF2)')
            except NotImplementedError:
                try:
                    # prevent race conditions when creating tmp files
                    temp_dir = tempfile.mkdtemp(dir=os.path.dirname(self.filename))
                    temp_out = os.path.join(temp_dir, 'qpdf_out.pdf')

                    # Will raise if this call is unsuccessful
                    check_call(['qpdf', "--password=", '--decrypt', self.filename, temp_out])

                    shutil.move(temp_out, self.filename)
                    self.parser_logger.info('File Decrypted (qpdf)')

                    pdf_binary = open(self.filename, 'rb')
                    pdf_reader = p2.PdfFileReader(pdf_binary)
                finally:
                    # Delete tmp files
                    shutil.rmtree(temp_dir)

        content = ""
        num_pages = pdf_reader.getNumPages()
        for i in range(num_pages):
            content += pdf_reader.getPage(i).extractText() + "\n"
        content = " ".join(content.replace(u"\xa0", " ").strip().split())
        
        with open("delete1.txt", "a") as f:
            f.write(content)

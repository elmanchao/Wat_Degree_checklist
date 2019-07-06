import os
import shutil
import tempfile
from subprocess import check_call
import PyPDF2 as p2
from setup_logger import SetupLogger


class TranscriptParser:
    def __init__(self, filename):
        self.filename = filename
        self.parser_logger = SetupLogger('transcript_parser.log', True)

    def get_name(self):
        pass

    def get_student_id(self):
        pass

    def decrypt_pdf(self, pdf_reader):
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

    def parse(self):
        pdf_binary = open(self.filename, 'rb')
        pdf_reader = p2.PdfFileReader(pdf_binary)
        
        if pdf_reader.isEncrypted:
            # self.decrypt_pdf(pdf_reader)
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

        num_pages = pdf_reader.getNumPages()

        for p_num in range(num_pages):
            p = pdf_reader.getPage(p_num)
            print(p.extractText())

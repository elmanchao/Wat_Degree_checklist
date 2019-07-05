import PyPDF2 as p2


class TranscriptParser:
    def __init__(self, transcript_binary):
        self.transcript_binary = transcript_binary

    def get_name(self):
        pass

    def get_student_id(self):
        pass

    def parse(self):
        pdf_reader = p2.PdfFileReader(self.transcript_binary)

        num_pages = pdf_reader.getNumPages()

        for p_num in range(num_pages):
            p = pdf_reader.getPage(p_num)
            print(p.extractText())

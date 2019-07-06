from flask import request, render_template, redirect, url_for, make_response
from flask_restful import Resource
from werkzeug.utils import secure_filename
import uuid

from models.transcript import TranscriptModel
from transcript_parser import TranscriptParser
from setup_logger import SetupLogger


class Transcript(Resource):
    def __init__(self):
        self.debug_logger = SetupLogger('transcript.log', True)

    def post(self):
        f = request.files['transcript']
        filename = secure_filename(f.filename)
        unique_pdf_name = str(uuid.uuid4())+'.pdf'
        f.save(unique_pdf_name)

        file_data = f.read()
        transcript = TranscriptModel(20426480, file_data)

        transcript_parser = TranscriptParser(unique_pdf_name)

        try:
            transcript_parser.parse()
            transcript.save_to_db()
        except Exception as e:
            self.debug_logger.error('Transcript post failed with error: {}'.format(e))
            # TODO: provide reason for failure.
            return redirect('/', code=303)

        # TODO: need to load correct checklist
        return redirect(url_for('transcript'), code=303)

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('2018-2019_BCS_AI.j2'), 200, headers)

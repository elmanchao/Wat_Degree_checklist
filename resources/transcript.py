from flask import request, render_template, redirect, url_for, make_response
from flask_restful import Resource
from werkzeug.utils import secure_filename

from models.transcript import TranscriptModel
from transcript_parser import TranscriptParser
from setup_logger import SetupLogger


class Transcript(Resource):
    def __init__(self):
        self.debug_logger = SetupLogger('transcript.log', True)

    def post(self):
        f = request.files['transcript']
        filename = secure_filename(f.filename)
        file_data = f.read()

        transcript = TranscriptModel(20426480, file_data)

        transcript_parse = TranscriptParser(file_data)
        
        try:
            transcript_parse.parse()
            transcript.save_to_db()
        except Exception as e:
            self.debug_logger.error('Transcript post failed with error: {}'.format(e))
            return redirect('/', code=303)

        return redirect(url_for('transcript'), code=303)

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('2018-2019_BCS_AI.j2'), 200, headers)

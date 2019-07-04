from flask import request, render_template, redirect, url_for, make_response
from flask_restful import Resource
from models.transcript import TranscriptModel
from werkzeug.utils import secure_filename


class Transcript(Resource):
    def post(self):
        f = request.files['transcript']

        filename = secure_filename(f.filename)

        transcript = TranscriptModel(20426480, f.read())
        try:
            transcript.save_to_db()
        except:
            print('exception')
            return redirect('/', code=303)

        f.save(filename)
        return redirect(url_for('transcript'), code=303)

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('2018-2019_BCS_AI.j2'), 200, headers)

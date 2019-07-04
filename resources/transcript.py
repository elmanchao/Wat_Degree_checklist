from flask import request, render_template, redirect, url_for
from flask_restful import Resource
from models.transcript import TranscriptModel
from werkzeug.utils import secure_filename


class Transcript(Resource):
    def post(self):
        f = request.files['transcript']

        filename = secure_filename(f.filename)

        # newFile = FileContents(name=filename, data=file.read())
        transcript = TranscriptModel(20426480, f.read())
        # try:
        transcript.save_to_db()
        # except:
            # print('exception')
            # return redirect('/')
        # db.session.add(newFile)
        # db.session.commit()

        f.save(filename)
        return redirect('http://google.ca')
        # return render_template('transcript_upload.j2')

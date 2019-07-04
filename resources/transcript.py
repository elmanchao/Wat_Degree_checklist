from flask import request, render_template
from flask_restful import Resource
from models.transcript import TranscriptModel
from werkzeug.utils import secure_filename


class Transcript(Resource):
    def post(self):
        f = request.files['transcript']

        filename = secure_filename(f.filename)

        # newFile = FileContents(name=filename, data=file.read())
        # db.session.add(newFile)
        # db.session.commit()

        f.save(filename)
        return 'file: {} successfully uploaded!'.format(filename)

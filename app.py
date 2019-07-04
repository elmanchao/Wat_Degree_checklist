import os

from flask import Flask, request, render_template, url_for
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


from resources.transcript import Transcript


app = Flask(__name__)
print("<<<<<<<<<<<<<<<<<<<<<{}".format(os.environ.get('DATABASE_URL', 'sqlite:///data.db')))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(Transcript, '/transcript')


@app.route('/')
def index():
    return render_template('transcript_upload.j2')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['transcript']

#         filename = secure_filename(f.filename)

#         newFile = FileContents(name=filename, data=file.read())
#         db.session.add(newFile)
#         db.session.commit()

#         f.save(secure_filename(f.filename))
#         return 'file: {} successfully uploaded!'.format(filename)


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

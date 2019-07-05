import os

from flask import Flask, request, render_template, url_for
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from resources.transcript import Transcript


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Transcript, '/transcript')


@app.route('/')
def index():
    return render_template('transcript_upload.j2')


if __name__ == "__main__":
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)

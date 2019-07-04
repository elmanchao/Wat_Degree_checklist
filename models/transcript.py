import sqlite3
from db import db


class TranscriptModel(db.Model):
    __tablename__ = 'transcripts'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    transcript_pdf = db.Column(db.LargeBinary)

    def __init__(self, student_id, transcript_pdf):
        self.student_id = student_id
        self.transcript_pdf = transcript_pdf

    @classmethod
    def find_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

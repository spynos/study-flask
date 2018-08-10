from db import db

class CaseModel(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    birth = db.Column(db.Integer)

    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'))
    library = db.relationship('LibraryModel')

    def __init__(self, name, birth, library_id):
        self.name = name
        self.birth = birth
        self.library_id = library_id

    def json(self):
        return {'name': self.name, 'birth': self.birth}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

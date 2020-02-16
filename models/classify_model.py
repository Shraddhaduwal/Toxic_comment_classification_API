import json

from sqlalchemy.ext import mutable
from db import db


# model class
class ClassifyModel(db.Model):
    __tablename__ = 'toxic_comment_classification_db'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, unique=True)
    comment = db.Column(db.String(10000))

    def __init__(self, comment_id, comment):
        self.comment_id = comment_id
        self.comment = comment

    def json(self):
        return {'comment_id': self.comment_id,
                'comment': self.comment}

    @classmethod
    def find_by_comment_id(cls, comment_id):
        return cls.query.filter_by(comment_id=comment_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            print(value)
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonEncodedDict)

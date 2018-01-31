from .. import db


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    icon_name = db.Column(db.String(128))
    short_name = db.Column(db.String(128))
    description = db.Column(db.String(1000))
    type = db.Column(db.String(128))
    free_response = db.Column(db.Boolean, default=False)
    answers = db.relationship("Answer", backref="question")

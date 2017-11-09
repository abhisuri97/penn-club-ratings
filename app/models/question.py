from .. import db


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    max_rating = db.Column(db.Integer)
    free_response = db.Column(db.Boolean, default=False)
    answers = db.relationship("Answer", backref="question")

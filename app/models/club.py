from .. import db


class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.String(db.String(1000))
    answer = db.relationship('Answer', backref='club')

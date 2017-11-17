from .. import db


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))

    @staticmethod
    def newAnswer(answer, rating, user_id, question_id, club_id):
        a = Answer.query.filter_by(user_id=user_id,club_id=club_id, 
                question_id=question_id).first() 
        if a is not None:
            db.session.delete(a)
            db.session.commit()

        a_new = Answer(answer=answer, rating=rating, user_id=user_id,
                question_id=question_id, club_id=club_id)
        db.session.add(a_new)
        db.session.commit()
        

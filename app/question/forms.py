from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, IntegerField, SelectField


class NewQuestionForm(Form):
    content = StringField('Please input the text of the question')
    max_rating = IntegerField('Please input the maximum on a scale of 1 to maximum you want this question to be rated out of')
    free_response = SelectField('Allow an optional response?', choices=[('True', 'Yes'), ('False', 'No')])
    submit = SubmitField('Create Question')

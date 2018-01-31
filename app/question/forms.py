from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, SelectField


class NewQuestionForm(Form):
    content = StringField('Please input the text of the question')
    short_name = StringField('Please input the short name of the question')
    icon_name = StringField('Please input the name of the icon for the question')
    description = StringField('Please input the description of the question')
    type = SelectField(
        'Question Type',
        choices=[('Numerical', 'Numerical'), ('Rating', 'Rating')])
    free_response = SelectField(
        'Allow an optional response?',
        choices=[('True', 'Yes'), ('False', 'No')])
    submit = SubmitField('Create Question')

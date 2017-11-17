from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired

from .. import db
from ..models import ClubCategory


class NewClubForm(Form):
    name = StringField('Please input the name of the club')
    desc = TextAreaField('Please input the description of the club')
    categories = QuerySelectMultipleField(
        'Add categories for club',
        validators=[InputRequired()],
        get_label='category_name',
        query_factory=lambda: db.session.query(ClubCategory).order_by('category_name'))
    submit = SubmitField('Create Club')

class EditClubForm(NewClubForm):
    is_confirmed = SelectField('Please indicate whether this club entry should be shown',
            choices=[('True', 'Yes'), ('False', 'No')])
    submit = SubmitField('Create')

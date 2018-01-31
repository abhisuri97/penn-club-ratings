from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired

from .. import db
from ..models import ClubCategory, User


class NewClubForm(Form):
    name = StringField('Please input the name of the club')
    img_link = StringField('Please a link to a banner image for the club')
    website = StringField('Please a link to the website for the club')
    desc = TextAreaField('Please input the description of the club')
    recruitment_info = TextAreaField('Please input any recruitment information about the club')
    categories = QuerySelectMultipleField(
        'Add categories for club',
        get_label='category_name',
        query_factory=
        lambda: db.session.query(ClubCategory).order_by('category_name'))
    submit = SubmitField('Create Club')


class EditClubForm(NewClubForm):
    owner = QuerySelectField('Select administrator for this club', get_label='email', query_factory=lambda: db.session.query(User).order_by('email'))
    is_confirmed = SelectField(
        'Please indicate whether this club entry should be shown',
        choices=[('True', 'Yes'), ('False', 'No')])
    submit = SubmitField('Edit Club')

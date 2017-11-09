from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired

from .. import db
from ..models import ClubCategory


class NewClubForm(Form):
    name = StringField('Please input the name of the club')
    categories = QuerySelectMultipleField(
        'Add categories for club',
        validators=[InputRequired()],
        get_label='category_name',
        query_factory=lambda: db.session.query(ClubCategory).order_by('category_name'))
    submit = SubmitField('Create Club')

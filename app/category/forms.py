from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms import ValidationError

from ..models import ClubCategory


class NewClubCategoryForm(Form):
    category_name = StringField('Please input the name of the new category')
    submit = SubmitField('Create Category')

    def validate_category_name(self, field):
        if ClubCategory.query.filter_by(category_name=field.data).first():
            raise ValidationError('Category Name already exists.')

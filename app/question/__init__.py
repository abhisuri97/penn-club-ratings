from flask import Blueprint

question = Blueprint('question', __name__)

from . import views  # noqa

from flask import Blueprint

club = Blueprint('club', __name__)

from . import views  # noqa

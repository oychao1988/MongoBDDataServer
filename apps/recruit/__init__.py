from flask import Blueprint

recruit_bp = Blueprint('recruit_bp', __name__, url_prefix='/recruits')

from .views import *
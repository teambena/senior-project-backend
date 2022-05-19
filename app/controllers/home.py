from flask import Blueprint, render_template
from app import *


Home_blueprint = Blueprint('Home', __name__)


@Home_blueprint.route('/')
@Home_blueprint.route('/index')
@jwt_required()
def home():
    return render_template('pages/home/index.html')

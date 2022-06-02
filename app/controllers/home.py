from flask import Blueprint, render_template
from app import *


Home_blueprint = Blueprint('Home', __name__)


@Home_blueprint.route('/')
@Home_blueprint.route('/index')
@jwt_required()
def home():
    user_role = current_user.get_role()
    pages = ['calendar']
    if user_role in pages:
        return render_template('pages/home/{0}.html'.format(user_role))
    else:
        return render_template('pages/home/index.html')

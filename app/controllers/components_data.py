
from flask import Blueprint
from app import *


Components_Data_blueprint = Blueprint('components_data', __name__)


from ..models.manager import Manager


@Components_Data_blueprint.route('/manager_username_exist/<value>')
@jwt_required(optional=True)
def manager_username_exist(value = None):
    try:
        rec_exist = utils.is_unique(Manager, "username", value)
        if rec_exist:
            return jsonify("true")
        return jsonify("false")
    except Exception as ex:
        return InternalServerError(ex)


@Components_Data_blueprint.route('/manager_email_exist/<value>')
@jwt_required(optional=True)
def manager_email_exist(value = None):
    try:
        rec_exist = utils.is_unique(Manager, "email", value)
        if rec_exist:
            return jsonify("true")
        return jsonify("false")
    except Exception as ex:
        return InternalServerError(ex)

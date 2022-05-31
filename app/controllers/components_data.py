
from flask import Blueprint
from app import *


Components_Data_blueprint = Blueprint('components_data', __name__)




@Components_Data_blueprint.route('/customer_option_list')
@jwt_required(optional=True)
def customer_option_list():
    try:
        sqltext = text(f"""SELECT customer_name AS value,customer_name AS label FROM Customer WHERE uid=:manager_id""")
        query_params = dict()
        query_params['manager_id'] = current_user.manager_id;
        arr = db.session.execute(sqltext, query_params)
        
        return jsonify([dict(row) for row in arr])
    except Exception as ex:
        return InternalServerError(ex)
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

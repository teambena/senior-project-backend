
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




@Components_Data_blueprint.route('/linechart_newchart1')
@jwt_required(optional=True)
def linechart_newchart1():
    try:
        sqltext = text(f"""SELECT  COUNT(Appointment.customer) AS count_of_customer, Appointment.start_date FROM Appointment WHERE uid=:manager_id GROUP BY Appointment.start_date ORDER BY Appointment.start_date ASC""")
        query_params = dict()
        query_params['manager_id'] = current_user.manager_id;
        arr = db.session.execute(sqltext, query_params)
        records = [row for row in arr]
        labels = [r["start_date"] for r in records]
        datasets = []
        dataset = dict(
            data = [r["count_of_customer"] for r in records],
            label = "Customer",
			backgroundColor = "rgba(0 , 128 , 64, 0.5)", 
			borderColor = "rgba(0 , 64 , 0, 0.5)", 
			borderWidth = "8",
        )
        datasets.append(dataset)
        
        return jsonify(dict(labels = labels, datasets = datasets))
    except Exception as ex:
        return InternalServerError(ex)

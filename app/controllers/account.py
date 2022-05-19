from flask import Blueprint
from app import *
from ..models.manager import *


Account_blueprint = Blueprint('account', __name__)


# View user account detail
@Account_blueprint.route('/')
@Account_blueprint.route('/index')
@jwt_required()
def view():
    try:
        rec_id = current_user.manager_id
        query = Manager.query.filter(Manager.manager_id == rec_id)
        query = query.with_entities(
            Manager.manager_id,
            Manager.name,
            Manager.username,
            Manager.email,
            Manager.business_name,
            Manager.business_phone_number,
            Manager.business_address,
            Manager.credit
        )
        
        record = query.first()
        if not record: return ResourceNotFound()
         
        record = record._asdict()
        
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Update user account detail
@Account_blueprint.route('/edit', methods=['GET', 'POST'])
@jwt_required()
def edit():
    try:
        rec_id = current_user.manager_id
        record = Manager.query.filter(Manager.manager_id == rec_id).first()
        if not record: return ResourceNotFound()
        
        if request.method == 'POST':
            modeldata = request.body
            errors = []
            form = ManagerAccountEditForm(modeldata, obj=record)
            
            if not form.validate():
                errors.append(form.errors)
            
            if errors:
                return BadRequest(errors)
            
            # save Manager record
            form.populate_obj(record)
            db.session.commit()
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


@Account_blueprint.route('/currentuserdata')
@jwt_required()
def currentuserdata():
    user = current_user._asdict()
    del user['password']
    return jsonify(user)


# Change user password
@Account_blueprint.route('/changepassword', methods=['POST'])
@jwt_required()
def changepassword():
    try:
        modeldata = request.body
        form = ChangePasswordForm(modeldata)
        if not form.validate():
            return BadRequest(form.errors)
        
        user = Manager.query.filter(Manager.manager_id == current_user.manager_id).first()
        current_password = modeldata['oldpassword']
        
        if not utils.check_password(user.password, current_password):
            return BadRequest("Current password is incorrect")
        
        user.password = utils.hash_password(modeldata['newpassword'])
        db.session.commit()
        
        return jsonify("Password change completed")
    except Exception as ex:
        return InternalServerError(ex)

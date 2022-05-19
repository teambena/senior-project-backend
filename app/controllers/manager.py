from flask import Blueprint
from app import *
from ..models.manager import *


Manager_blueprint = Blueprint('Manager', __name__)


# list Manager records
# @param fieldname: filter table records by a field
# @param fieldvalue:  filter value
# @request.args search: search records
# @request.args orderby: sort records by field name
# @request.args ordertype: sort type (asc|desc)
# @request.args page: current page number
# @request.args limit: maximum number of records to select
@Manager_blueprint.route('/index')
@Manager_blueprint.route('/')
@Manager_blueprint.route('/index/<fieldname>')
@Manager_blueprint.route('/index/<fieldname>/<fieldvalue>')
@jwt_required()
def index(fieldname=None, fieldvalue=None):
    try:
        query = Manager.query
        search = request.args.get('search')
        if search:
            query = query.filter(
                Manager.name.like(f'%{search}%') | 
                Manager.username.like(f'%{search}%') | 
                Manager.email.like(f'%{search}%') | 
                Manager.business_name.like(f'%{search}%') | 
                Manager.business_address.like(f'%{search}%') 
            )
        
        # filter by dynamic field name
        if fieldname:
            field_filter = text(f'{fieldname} = :fieldvalue').params(fieldvalue=fieldvalue)
            query = query.filter(field_filter)
        
        orderby = request.args.get('orderby')
        ordertype = request.args.get('ordertype', 'desc')
        if orderby:
            query = query.order_by(text(f'{orderby} {ordertype}'))
        else:
            query = query.order_by(text(f'Manager.manager_id {ordertype}'))
        
        # fields to select
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
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', MAX_RECORD_COUNT))
        offset = ((page-1) * limit)
        total_records = query.count()
        records = query.limit(limit).offset(offset).all()
        record_count = len(records)
        total_pages = round(total_records/limit)
        records = [(row._asdict()) for row in records]
        
        # response object
        response = dict(
            records=records, 
            total_records=total_records,
            record_count=record_count,
            total_pages=total_pages
        )
        return jsonify(response)
    except Exception as ex:
        return InternalServerError(ex)


# Select table record by ID
@Manager_blueprint.route('/view/<rec_id>')
@jwt_required()
def view(rec_id=None):
    try:
        query = Manager.query
        query = query.filter(Manager.manager_id == rec_id)
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
        
        # return result as json
        return jsonify(record)
        
    except Exception as ex:
        return InternalServerError(ex)


# Save form data to the Manager table
@Manager_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add():
    try:
        modeldata = request.body
        form = ManagerAddForm(modeldata)
        errors = [] # list of validation errors
        
        # validate manager form data
        if not form.validate():
            errors.append(form.errors)
        
        if errors:
            return BadRequest(errors)
        
        record = Manager()
        form.populate_obj(record)

        # check if username record already exist in the database
        rec_value = str(modeldata['username'])
        rec_exist = utils.is_unique(Manager, "username", rec_value)
        if rec_exist:
            return BadRequest(rec_value + " Already exist!")

        # check if email record already exist in the database
        rec_value = str(modeldata['email'])
        rec_exist = utils.is_unique(Manager, "email", rec_value)
        if rec_exist:
            return BadRequest(rec_value + " Already exist!")
        record.password = utils.hash_password(modeldata['password'])
        
        # save manager records
        db.session.add(record)
        db.session.commit()
        db.session.flush()
        rec_id = record.manager_id
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Select record by table primary key and update with form data
@Manager_blueprint.route('/edit/<rec_id>', methods=['GET', 'POST'])
@jwt_required()
def edit(rec_id=None):
    try:
        query = Manager.query
        query = query.filter(Manager.manager_id == rec_id)
        record = query.first()
        if not record: return ResourceNotFound()
        
        if request.method == 'POST':
            errors = []
            modeldata = request.body
            form = ManagerEditForm(modeldata, obj=record)
            
            if not form.validate():
                errors.append(form.errors)
            # check if username already exist in the database
            rec_value = str(modeldata['username'])
            rec_exist = utils.is_unique(Manager, "username", rec_value, "manager_id", rec_id)
            if rec_exist:
                return BadRequest(rec_value  + " Already exist!")
            
            if errors:
                return BadRequest(errors)
            
            # save Manager record
            form.populate_obj(record)
            db.session.commit()
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Delete record from the database
# Support multi delete by separating record id by comma.
@Manager_blueprint.route('/delete/<rec_id>')
@jwt_required()
def delete(rec_id):
    query = Manager.query
    arr_id = rec_id.split(',')
    try:
        query = query.filter(Manager.manager_id.in_(arr_id))
        query.delete(synchronize_session=False)
        db.session.commit()
        
        return jsonify(arr_id)
    except Exception as ex:
        return InternalServerError(ex)

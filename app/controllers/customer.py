from flask import Blueprint
from app import *
from ..models.customer import *


Customer_blueprint = Blueprint('Customer', __name__)


# list Customer records
# @param fieldname: filter table records by a field
# @param fieldvalue:  filter value
# @request.args search: search records
# @request.args orderby: sort records by field name
# @request.args ordertype: sort type (asc|desc)
# @request.args page: current page number
# @request.args limit: maximum number of records to select
@Customer_blueprint.route('/index')
@Customer_blueprint.route('/')
@Customer_blueprint.route('/index/<fieldname>')
@Customer_blueprint.route('/index/<fieldname>/<fieldvalue>')
@jwt_required()
def index(fieldname=None, fieldvalue=None):
    try:
        query = Customer.query
        search = request.args.get('search')
        if search:
            query = query.filter(
                Customer.customer_name.like(f'%{search}%') | 
                Customer.customer_email.like(f'%{search}%') | 
                Customer.uid.like(f'%{search}%') 
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
            order = text('Customer.customer_name ASC')
            query = query.order_by(order)
        
        # fields to select
        query = query.with_entities(
            Customer.customer_id,
            Customer.customer_name,
            Customer.customer_email,
            Customer.customer_phone_number,
            Customer.uid
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
@Customer_blueprint.route('/view/<rec_id>')
@jwt_required()
def view(rec_id=None):
    try:
        query = Customer.query
        query = query.filter(Customer.customer_id == rec_id)
        query = query.with_entities(
            Customer.customer_id,
            Customer.customer_name,
            Customer.customer_email,
            Customer.customer_phone_number,
            Customer.uid
        )
        
        record = query.first()
        if not record: return ResourceNotFound()
         
        record = record._asdict()
        
        # return result as json
        return jsonify(record)
        
    except Exception as ex:
        return InternalServerError(ex)


# Save form data to the Customer table
@Customer_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add():
    try:
        modeldata = request.body
        form = CustomerAddForm(modeldata)
        errors = [] # list of validation errors
        
        # validate customer form data
        if not form.validate():
            errors.append(form.errors)
        
        if errors:
            return BadRequest(errors)
        
        record = Customer()
        form.populate_obj(record)
        
        # save customer records
        db.session.add(record)
        db.session.commit()
        db.session.flush()
        rec_id = record.customer_id
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Select record by table primary key and update with form data
@Customer_blueprint.route('/edit/<rec_id>', methods=['GET', 'POST'])
@jwt_required()
def edit(rec_id=None):
    try:
        query = Customer.query
        query = query.filter(Customer.customer_id == rec_id)
        record = query.first()
        if not record: return ResourceNotFound()
        
        if request.method == 'POST':
            errors = []
            modeldata = request.body
            form = CustomerEditForm(modeldata, obj=record)
            
            if not form.validate():
                errors.append(form.errors)
            
            if errors:
                return BadRequest(errors)
            
            # save Customer record
            form.populate_obj(record)
            db.session.commit()
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Delete record from the database
# Support multi delete by separating record id by comma.
@Customer_blueprint.route('/delete/<rec_id>')
@jwt_required()
def delete(rec_id):
    query = Customer.query
    arr_id = rec_id.split(',')
    try:
        query = query.filter(Customer.customer_id.in_(arr_id))
        query.delete(synchronize_session=False)
        db.session.commit()
        
        return jsonify(arr_id)
    except Exception as ex:
        return InternalServerError(ex)

from flask import Blueprint
from app import *
from ..models.appointment import *


Appointment_blueprint = Blueprint('Appointment', __name__)


# list Appointment records
# @param fieldname: filter table records by a field
# @param fieldvalue:  filter value
# @request.args search: search records
# @request.args orderby: sort records by field name
# @request.args ordertype: sort type (asc|desc)
# @request.args page: current page number
# @request.args limit: maximum number of records to select
@Appointment_blueprint.route('/index')
@Appointment_blueprint.route('/')
@Appointment_blueprint.route('/index/<fieldname>')
@Appointment_blueprint.route('/index/<fieldname>/<fieldvalue>')
@jwt_required()
def index(fieldname=None, fieldvalue=None):
    try:
        query = Appointment.query
        search = request.args.get('search')
        if search:
            query = query.filter(
                Appointment.customer.like(f'%{search}%') | 
                Appointment.start_date.like(f'%{search}%') 
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
            query = query.order_by(text(f'Appointment.appointment_id {ordertype}'))
        
        # fields to select
        query = query.with_entities(
            Appointment.appointment_id,
            Appointment.customer,
            Appointment.start_date,
            Appointment.start_time,
            Appointment.end_date,
            Appointment.end_time,
            Appointment.description,
            Appointment.uid
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
@Appointment_blueprint.route('/view/<rec_id>')
@jwt_required()
def view(rec_id=None):
    try:
        query = Appointment.query
        query = query.filter(Appointment.appointment_id == rec_id)
        query = query.with_entities(
            Appointment.appointment_id,
            Appointment.customer,
            Appointment.start_date,
            Appointment.start_time,
            Appointment.end_date,
            Appointment.end_time,
            Appointment.description,
            Appointment.uid
        )
        
        record = query.first()
        if not record: return ResourceNotFound()
         
        record = record._asdict()
        
        # return result as json
        return jsonify(record)
        
    except Exception as ex:
        return InternalServerError(ex)


# Save form data to the Appointment table
@Appointment_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add():
    try:
        modeldata = request.body
        form = AppointmentAddForm(modeldata)
        errors = [] # list of validation errors
        
        # validate appointment form data
        if not form.validate():
            errors.append(form.errors)
        
        if errors:
            return BadRequest(errors)
        
        record = Appointment()
        form.populate_obj(record)
        record.uid = "1"
        
        # save appointment records
        db.session.add(record)
        db.session.commit()
        db.session.flush()
        rec_id = record.appointment_id
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Select record by table primary key and update with form data
@Appointment_blueprint.route('/edit/<rec_id>', methods=['GET', 'POST'])
@jwt_required()
def edit(rec_id=None):
    try:
        query = Appointment.query
        query = query.filter(Appointment.appointment_id == rec_id)
        record = query.first()
        if not record: return ResourceNotFound()
        
        if request.method == 'POST':
            errors = []
            modeldata = request.body
            form = AppointmentEditForm(modeldata, obj=record)
            
            if not form.validate():
                errors.append(form.errors)
            
            if errors:
                return BadRequest(errors)
            
            # save Appointment record
            form.populate_obj(record)
            db.session.commit()
         
        record = record._asdict()
        return jsonify(record)
    except Exception as ex:
        return InternalServerError(ex)


# Delete record from the database
# Support multi delete by separating record id by comma.
@Appointment_blueprint.route('/delete/<rec_id>')
@jwt_required()
def delete(rec_id):
    query = Appointment.query
    arr_id = rec_id.split(',')
    try:
        query = query.filter(Appointment.appointment_id.in_(arr_id))
        query.delete(synchronize_session=False)
        db.session.commit()
        
        return jsonify(arr_id)
    except Exception as ex:
        return InternalServerError(ex)

from app import db,  OptionalButNotEmpty, datetime, timedelta, config
from wtforms import Form, StringField, FloatField, IntegerField, BooleanField, DateField
from wtforms.validators import *


class Appointment(db.Model):
    __tablename__ = 'Appointment'
    customer = db.Column("customer", db.String)
    start_date = db.Column("start_date", db.DATE)
    start_time = db.Column("start_time", db.String)
    end_date = db.Column("end_date", db.DATE)
    end_time = db.Column("end_time", db.String)
    description = db.Column("description", db.String)
    uid = db.Column("uid", db.String)
    status = db.Column("status", db.String)
    appointment_id = db.Column("appointment_id", db.Integer, primary_key=True, autoincrement=True)
    
    def _asdict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AppointmentAddForm(Form):
    customer = StringField('Customer', [])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = StringField('Start Time', [])
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = StringField('End Time', [])
    description = StringField('Description', [])
    uid = StringField('Uid', [])
    status = StringField('Status', [])


class AppointmentEditForm(Form):
    customer = StringField('Customer', [])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = StringField('Start Time', [])
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = StringField('End Time', [])
    description = StringField('Description', [])
    status = StringField('Status', [])

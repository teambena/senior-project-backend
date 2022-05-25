from app import db,  OptionalButNotEmpty, datetime, timedelta, config
from wtforms import Form, StringField, FloatField, IntegerField, BooleanField
from wtforms.validators import *


class Customer(db.Model):
    __tablename__ = 'Customer'
    customer_name = db.Column("customer_name", db.String)
    customer_email = db.Column("customer_email", db.String)
    customer_phone_number = db.Column("customer_phone_number", db.Integer)
    uid = db.Column("uid", db.String)
    customer_id = db.Column("customer_id", db.Integer, primary_key=True, autoincrement=True)
    
    def _asdict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CustomerAddForm(Form):
    customer_name = StringField('Customer Name', [])
    customer_email = StringField('Customer Email', [Email()])
    customer_phone_number = FloatField('Customer Phone Number', [NumberRange()])
    uid = StringField('Uid', [])


class CustomerEditForm(Form):
    customer_name = StringField('Customer Name', [])
    customer_email = StringField('Customer Email', [Email()])
    customer_phone_number = FloatField('Customer Phone Number', [NumberRange()])

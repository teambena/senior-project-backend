from app import db,  OptionalButNotEmpty, datetime, timedelta, config
from wtforms import Form, StringField, FloatField, IntegerField, BooleanField
from wtforms.validators import *


class Manager(db.Model):
    __tablename__ = 'Manager'
    name = db.Column("name", db.String)
    username = db.Column("username", db.String)
    email = db.Column("email", db.String)
    password = db.Column("password", db.String)
    business_name = db.Column("business_name", db.String)
    business_phone_number = db.Column("business_phone_number", db.Integer)
    business_address = db.Column("business_address", db.String)
    credit = db.Column("credit", db.Integer)
    manager_id = db.Column("manager_id", db.Integer, primary_key=True, autoincrement=True)

    def has_verified_email(self):
        if self.email_verified_at is None:
            return False
        return True

    def set_email_verified(self):
        self.email_verified_at = datetime.now()

    def get_id(self):
        return str(self.manager_id)

    def get_name(self):
        return str(self.username)

    def get_role(self):
        return ''

    def get_role_name(self):
        rbac = Rbac(self.get_role())
        roles = rbac.user_role_names
        if roles:
            return str(roles[0]).lower()
        return None

    def get_email(self):
        return str(self.email)

    def get_photo(self):
        return ''
    
    def _asdict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PasswordForm(Form):
    confirm_password = StringField('Confirm password', [InputRequired()])
    password = StringField('New Password', [InputRequired(), EqualTo('confirm_password', message='Passwords confirmation does not match')])


class ChangePasswordForm(Form):
    oldpassword = StringField('Old password', [InputRequired()])
    confirmpassword = StringField('Confirm password', [InputRequired()])
    newpassword = StringField('New Password', [InputRequired(), EqualTo('confirmpassword', message='Passwords confirmation does not match')])


class ManagerRegisterForm(Form):
    name = StringField('Name', [])
    username = StringField('Username', [InputRequired()])
    email = StringField('Email', [InputRequired(),Email()])
    password = StringField('Password', [InputRequired()])
    confirm_password = StringField('Confirm password', [InputRequired(), EqualTo('password', message='Passwords confirmation does not match')])
    business_name = StringField('Business Name', [])
    business_phone_number = FloatField('Business Phone Number', [NumberRange()])
    business_address = StringField('Business Address', [])


class ManagerAccountEditForm(Form):
    name = StringField('Name', [])
    username = StringField('Username', [])
    business_name = StringField('Business Name', [])
    business_phone_number = FloatField('Business Phone Number', [NumberRange()])
    business_address = StringField('Business Address', [])
    credit = FloatField('Credit', [NumberRange()])


class ManagerAddForm(Form):
    username = StringField('Username', [InputRequired()])
    email = StringField('Email', [InputRequired(),Email()])
    password = StringField('Password', [InputRequired()])
    confirm_password = StringField('Confirm password', [InputRequired(), EqualTo('password', message='Passwords confirmation does not match')])
    business_phone_number = FloatField('Business Phone Number', [NumberRange()])


class ManagerEditForm(Form):
    name = StringField('Name', [])
    username = StringField('Username', [OptionalButNotEmpty()])
    business_name = StringField('Business Name', [])
    business_phone_number = FloatField('Business Phone Number', [NumberRange()])
    business_address = StringField('Business Address', [])
    credit = FloatField('Credit', [NumberRange()])

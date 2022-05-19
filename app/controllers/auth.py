from flask import Blueprint, redirect, render_template
from app import *
from flask_jwt_extended import create_access_token, decode_token
from ..models.manager import *


Auth_blueprint = Blueprint('index', __name__)


# create user auth token
def generate_user_token(user):
    user_id = user.manager_id
    expires_in = app.config["JWT_DURATION"]
    expires = timedelta(minutes=expires_in) # jwt lifetime duration
    token = create_access_token(identity=user_id, expires_delta=expires)
    return token


# decode token and return user id
def get_userid_from_jwt(token):
    payload = decode_token(token)
    return payload["sub"]




# Return user login data
def get_user_login_data(user):
    token = generate_user_token(user)
    user = user._asdict()
    del user['password'] # no need to return the password field
    return dict(token=token, user=user)


# Authenticate and return user login data
@Auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.body['username']
        password = request.body['password']
        query = Manager.query
        query = query.filter((Manager.username == username) | (Manager.email == username))
        user = query.first()
        if not user:
            return BadRequest("Username or password not correct") # username incorrect
        
        if not utils.check_password(user.password, password):
            return BadRequest("Username or password not correct") # password incorrect
        
        
        return jsonify(get_user_login_data(user))
    except Exception as ex:
        return InternalServerError(ex)


# Save new user record
@Auth_blueprint.route('/register', methods=['POST'])
def register():
    try:
        modeldata = request.body
        form = ManagerRegisterForm(modeldata)
        errors = [] # form validation errors
        
        # validate register form data
        if not form.validate():
            errors.append(form.errors)
        
        if errors:
            return BadRequest(errors)
        
        user = record = Manager()
        form.populate_obj(record)
        record.password = utils.hash_password(modeldata['password'])

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
        
        # save manager records
        db.session.add(record)
        db.session.commit()
        db.session.flush()
        rec_id = record.manager_id
        return jsonify(get_user_login_data(record))
    except Exception as ex:
        return InternalServerError(ex)


# send password reset link to user email
@Auth_blueprint.route('/forgotpassword', methods=['POST'])
def forgotpassword():
    try:
        modeldata = request.body
        email = modeldata['email']
        user = Manager.query.filter(Manager.email == email).first()
        if not user: 
            return ResourceNotFound("Email not registered")
        token = generate_user_token(user)
        site_addr = app.config['FRONTEND_ADDR']
        resetlink = f"{site_addr}/#/index/resetpassword?token={token}"
        username = user.username
        mailsubject = 'Password Reset'
        template_context = dict(pagetitle='Password reset', username=username, email=email, resetlink = resetlink)
        mailbody = render_template('pages/index/password_reset_email_template.html', **template_context)
        utils.send_mail(email, mailsubject, mailbody)
        
        return "We have emailed your password reset link!"
    except Exception as ex:
            return InternalServerError(ex)


# Reset user password
@Auth_blueprint.route('/resetpassword', methods=['POST'])
def resetpassword():
    try:
        modeldata = request.body
        token = modeldata['token']
        user_id = get_userid_from_jwt(token)
        form = PasswordForm(modeldata)
        if not form.validate():
            return BadRequest(form.errors)
        
        user = Manager.query.filter_by(manager_id=user_id).first()
        if not user:
            return BadRequest("Invalid Token")
        user.password = utils.hash_password(form.password.data)
        db.session.commit()
        
        return jsonify("Password changed")
    except Exception as ex:
        return InternalServerError(ex)

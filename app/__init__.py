from flask import Flask, request, json, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import func, text, literal_column, cast
from .helpers import jsonmultidict as json2dict
from .helpers.json_encoder import CustomJSONEncoder
from flask_mail import Mail
from flask_cors import CORS
from datetime import datetime, date, time, timedelta
import os
import flask_excel as excel
from flask_jwt_extended import JWTManager, jwt_required, current_user
app = Flask(__name__)
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')
app.url_map.strict_slashes = False
CORS(app)  # This will enable CORS for all routes
MAX_RECORD_COUNT = app.config['MAX_RECORD_COUNT']
ORDER_TYPE = app.config['ORDER_TYPE']
SITE_NAME = app.config['SITE_NAME']
DEBUG = app.config['DEBUG']

db = SQLAlchemy(app)  # init database

mail = Mail(app)  # init mail client
excel.init_excel(app)  # init flask_excel


from .helpers.utils import utils, OptionalButNotEmpty
from .helpers.http_errors import *

# Handle app exceptions
# Return 500 Internal Server Error
@app.errorhandler(500)
def server_error(msg):
    if DEBUG:
        print("\n" + str(msg) + "\n")
        return jsonify(str(msg)), 500 # return exception message in development mode
    else:
        print("\n" + str(msg) + "\n")
        return jsonify("Error processing request..."), 500

def resolve_request_body():
    # Before every request, resolve `request.body` from `request.get_json()`
    if request.method == 'POST':
        body = request.get_json()
        if body:
            if isinstance(body, list):
                allpost = []
                for post in body:
                    allpost.append(json2dict.get_json_multidict(post))
                request.body = allpost
            else:
                request.body = json2dict.get_json_multidict(body)
        else:
            request.body = json2dict.get_json_multidict(request.form)

app.before_request(resolve_request_body)
app.json_encoder = CustomJSONEncoder

jwt = JWTManager(app)
from .models.manager import Manager


@jwt.user_lookup_loader
def get_current_user(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = Manager.query.filter(Manager.manager_id == identity).first()
    return user

@jwt.unauthorized_loader
def unauthorized_handler(error):
    return Unauthorized(str(error))


@jwt.invalid_token_loader
def invalid_token_callback(token):
    return Unauthorized("Invalid Token")


from .controllers.home import  Home_blueprint
from .controllers.components_data import  Components_Data_blueprint
from .controllers.fileuploader import File_Uploader_blueprint
from .controllers.auth import Auth_blueprint
from .controllers.account import Account_blueprint
from .controllers.manager import Manager_blueprint


# Page controller blueprint
app.register_blueprint(Home_blueprint, url_prefix = "/api/home")
app.register_blueprint(Components_Data_blueprint, url_prefix = "/api/components_data")
app.register_blueprint(File_Uploader_blueprint, url_prefix = "/api/fileuploader")
app.register_blueprint(Auth_blueprint, url_prefix = "/api/auth")
app.register_blueprint(Account_blueprint, url_prefix = "/api/account")
app.register_blueprint(Manager_blueprint, url_prefix = "/api/manager")
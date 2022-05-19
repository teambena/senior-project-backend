from flask import request
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import StopValidation
from app import app, mail, datetime, time, text
from .uploader import Uploader
from wtforms.validators import ValidationError
import random
import locale
import uuid
import os
import mimetypes

class utils:

    # generate random color
    # example rgba(233,123,3,0.2)
    @staticmethod
    def random_color(opacity=1):
        r = int(random.random() * 256)
        g = int(random.random() * 256)
        b = int(random.random() * 256)
        return 'rgba({0},{1},{2},{3})'.format(r, g, b, opacity)
    
    # generate list of random color
    # example [rgba(233,123,3,0.2),... ]
    @staticmethod
    def arr_random_color(arrLen, opacity=1):
        colors = []
        for x in range(arrLen):
            colors.append(utils.random_color(opacity))
        return colors
    
    
    # Generate a Random String From Set Of supplied data context
    # example ekszlrc5apjx
    @staticmethod
    def random_str(limit=12, context='abcdefghijklmnopqrstuvwxyz1234567890'):
        l = limit if limit <= len(context) else len(context)
        return ''.join(random.sample(context, l))

    
    # Generate a Random String and characters From Set Of supplied data context
    # example !XQjKcu2r$^C
    @staticmethod
    def random_chars(limit=12, context='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*_+-='):
        l = limit if limit <= len(context) else len(context)
        return ''.join(random.sample(context, l))

    
    # Generate a Random String From Set Of supplied data context
    # example 783621
    @staticmethod
    def random_num(limit=6):
        range_start = 10**(limit-1)
        range_end = (10**limit)-1
        return random.randint(range_start, range_end)

    
    # Generates RFC 4122 compliant Version 4 UUIDs.
    @staticmethod
    def uuid():
        return str(uuid.uuid4())

    
    # format a value based on current locale
    # example $90,342
    @staticmethod
    def to_currency(amount, locale_currency='en-US'):
        locale.setlocale(locale.LC_ALL, locale_currency)
        locale.currency(amount, grouping=True)

    
    # return string date in human readable format
    # example 2, Dec 2018
    @staticmethod
    def human_date(strdate):
        return strdate.strftime('%d, %b %Y')

    
    # return string date in human readable format
    # example 2, Dec 2018 02:30pm
    @staticmethod
    def human_datetime(strdate):
        return strdate.strftime('%d, %b %Y %H:%M')

    
    # return string date in human readable format
    # example 02:30pm
    @staticmethod
    def human_time(strdate):
        return strdate.strftime('%H:%M')

    
    # return string date in relative format support both date string and timestamp
    # example 4 days ago , in 3 minutes, just now
    # for more info https://github.com/hustcc/timeago
    @staticmethod
    def relative_date(strtime=False):
        try:
            import timeago
            now = datetime.utcnow()
            rel_date = strtime
            if type(strtime) is int:
                rel_date = datetime.fromtimestamp(strtime)
            elif isinstance(strtime, datetime):
                rel_date = strtime
            return timeago.format(rel_date, now, utils.get_locale())
        except Exception as ex:
            return str(ex)
    
    
    # convert string to lower case
    # example This is PyRad » this is pyrad
    @staticmethod
    def str_lower(val):
        return str(val).lower()

    
    # convert string to lower case
    # example This is PyRad » THIS IS PYRAD
    @staticmethod
    def str_upper(val):
        return str(val).upper()

    
    # Return a copy of the string with its first character capitalized and the rest lowercased.
    # example This is PyRad » This is Pyrad
    @staticmethod
    def str_ucfirst(val):
        return str(val).capitalize()

    
    # Return a titlecased version of the string where words start with an uppercase character and the remaining characters are lowercase.
    # example This is PyRad » This is Pyrad
    @staticmethod
    def str_title(val):
        return str(val).title()

    
    # return current date
    # example 2018-02-12
    @staticmethod
    def date_now():
        now = datetime.now()
        return now.strftime('%Y-%m-%d')

    
    # return current time
    # example 02:12:45
    @staticmethod
    def time_now():
        now = datetime.now()
        return now.strftime('%H:%M:%S')

    
    # return unix timestamp
    # Example 1545566881
    @staticmethod
    def timestamp():
        return str(int(time.time()))

    
    # return current datetime
    # example 2018-02-12 02:12:45
    @staticmethod
    def datetime_now():
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    
    # return combine current request path with new path
    @staticmethod
    def set_url(path=''):
        return request.host_url + path.strip('/')


    # generate password hash
    @staticmethod
    def hash_password(password_text):
        return generate_password_hash(password_text)


    # validate password text
    @staticmethod
    def check_password(password_hash, password_text):
        try:
            return check_password_hash(password_hash, password_text)
        except:
            return False
    
    
    # delete files associated with a record when deleting the record
    @staticmethod
    def delete_record_files(file_path, field_name):
        file_paths = file_path.split(",")
        upload_setting = app.config["UPLOAD_SETTINGS"][field_name]
        resize_settings = upload_setting.get('image_resize', [])
        img_thumb_dirs = [d['name'] for d in resize_settings]
        img_exts = ["jpg", "png", "jpeg"]
        for path in file_paths:
            file = os.path.join(app.config['APP_ROOT'], path)
            if os.path.isfile(file):
                os.remove(file)
                file_ext = os.path.splitext(file)[1][1:].strip().lower()
                is_img = file_ext in img_exts
                if is_img:
                    for thumb_dir in img_thumb_dirs:
                        paths = file.split("/");
                        paths.insert(len(paths)-1, thumb_dir)
                        thumb_full_path = os.path.join(*paths)
                        if os.path.isfile(thumb_full_path):
                            os.remove(thumb_full_path)

    # move uploaded files from temp directory to destination directory
    @staticmethod
    def move_uploaded_files(files, fieldname):
        file_info = { 
            "filepath": "", 
            "filesize": "", 
            "filename": "", 
            "filetype": "", 
            "fileext": ""
        }
        if files:
            uploader = Uploader(files, fieldname)
            uploaded_files = uploader.move_uploaded_files()
            first_file = uploaded_files.split(",")[0]
            file = os.path.join(app.config['APP_ROOT'], first_file)
           
            file_info["filepath"] = uploaded_files
            
            if os.path.exists(file):
                file_info["filesize"] = os.path.getsize(file)
                file_info["filename"] = os.path.basename(file)
                file_info["fileext"] = os.path.splitext(file)[1][1:].strip().lower()
                mime =  mimetypes.guess_type(file)
                
                if mime:
                    file_info["filetype"] = mime[0]
        
        return file_info
    
    
    # convinient function for sending email. Please make sure that email configuration setings are provided in config.py
    @staticmethod
    def send_mail(email, subject, body):
        msg = Message(subject, recipients=[email], html=body)
        return mail.send(msg)


    # check if duplicate record already exit in the database
    @staticmethod
    def is_unique(model, field, fieldvalue, tablekey=None, recid=None):
        query = model.query
        field_filter = text(f'{field} = :fieldvalue').params(fieldvalue=fieldvalue)
        record = query.filter(field_filter).first()
        if record:
            record = record._asdict()
            if (tablekey is None or str(recid) != str(record[tablekey])):
                return True
        return False


class OptionalButNotEmpty(object):
    """
    Allows missing but not empty input and stops the validation chain from continuing.
    """
    field_flags = ('optional', )

    def __call__(self, form, field):
        if not field.raw_data:
            raise StopValidation()



class Unique(object):
    """ validator that checks if record already exists in a database table"""
    def __init__(self, model, field, id=None, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'Already exists'
        self.message = message

    def __call__(self, form, field):
        record = self.model.query.filter(self.field == field.data).first()
        pk = None
        if '__pk__' in form and '__recid__' in form:
            pk = form.__pk__
            recid = form.__recid__
        if record and (pk is None or recid != record[pk]):
            raise ValidationError(self.message)
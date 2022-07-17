import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
ASSETS_DIR = 'static'
APP_STATIC = os.path.join(APP_ROOT, ASSETS_DIR)

WKHTMLTOPDF_BIN_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # path to your wkhtmltopdf installation.
PDF_DIR_PATH = os.path.join(APP_STATIC, 'reports')

DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///D:\\All git\\atw\\ATW.sqlite'

CSRF_ENABLED = True

SECRET_KEY = 'deb4c1feaab2a3d468950c4ad834e902'
SECURITY_PASSWORD_SALT = '0ec5b7030a96948959ac18c6e52a0740'
SITE_NAME = 'ATW' 
SITE_ADDR = 'http://localhost:8060'
FRONTEND_ADDR = 'http://localhost:8050'
USER_APP_NAME = 'ATW'

# file upload directories 
UPLOAD_DIR = 'uploads/'
UPLOAD_TEMP_DIR = 'uploads/temp/'
UPLOAD_FILE_DIR = 'uploads/files/'
UPLOAD_IMG_DIR = 'uploads/photos/'
MAX_UPLOAD_FILESIZE = 90
MAX_CONTENT_LENGTH = 16777216  # 16 * 1024 * 1024 16mb you can change.
DEFAULT_PAGE = 'index'  # default controller class
DEFAULT_PAGE_ACTION = 'index'  # default controller action

# application page settings
HOME_PAGE = 'home'

# default supported languages
LANGUAGES = {'en': 'English', 'pt_PT': 'Portuguese', 'hi': 'Hindi', 'ar': 'Arabic', 'fr': 'Francais', 'it': 'Italian', 'es': 'Spanish', 'zh_CN': 'Chinese', 'ru': 'Russian', 'de': 'German'}
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

# email configuration default settings
MAIL_USERNAME = 'transmatter.team@outlook.com'
MAIL_PASSWORD = 'Tmat@1739'
MAIL_SERVER = 'smtp-mail.outlook.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# MAIL_SUPPRESS_SEND = False

# default email sender details
MAIL_DEFAULT_SENDER = 'transmatter.team@outlook.com'
DEFAULT_EMAIL_ACCOUNT_NAME = ''
USER_EMAIL_SENDER_NAME = ''
USER_EMAIL_SENDER_EMAIL = ''

# DB Values for user account status
ACCOUNT_ACTIVE = 'Active'
ACCOUNT_VERIFIED = 'Verified'
ACCOUNT_NOT_VERIFIED = 'Not Verified'
ACCOUNT_PENDING = 'Pending'
ACCOUNT_SUSPENDED = 'Suspended'

# Page Record Settings
MAX_RECORD_COUNT = 10  # default max records to retrieve  per page
ORDER_TYPE = 'desc'  # default order type. From the last record in the database

OTP_DURATION = 5  # OTP Duration in minutes

JWT_DURATION = 30  # OTP Duration in minutes

# Page upload settings
UPLOAD_SETTINGS = dict(
    import_data=dict(
        filename_type="timestamp",
        extensions="json,csv",
        limit=10,
        max_file_size=3,
        return_full_path="false",
        filename_prefix="",
        upload_dir="uploads/files/"
    ),
    
)
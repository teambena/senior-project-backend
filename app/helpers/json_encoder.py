from flask.json import JSONEncoder
from decimal import Decimal
from datetime import datetime, date, time, timedelta


# Add support for serializing decimal and date time
class CustomJSONEncoder(JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date) or isinstance(obj, time) or isinstance(obj, timedelta):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return super().default(obj)

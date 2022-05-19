from flask import jsonify
from app import DEBUG
import logging
class HttpError():
    status_code = 500
    message = "Internal server error"
    def __init__(self, message, status_code=None):
        self.message = message
        
    def abort(self):
        return jsonify(self.message), self.status_code

def BadRequest(message = "Bad Request"):
    return HttpError(message, 400).abort()

def Unauthorized(message = "Unauthorized"):
    return HttpError(message, 401).abort()

def AccessForbidden(message = "Access forbidden"):
    return HttpError(message, 403).abort()

def ResourceNotFound(message = "Page or record not found"):
    return HttpError(message, 404).abort()

def InternalServerError(ex = "Internal server error"):
    print("\n===================== Exception StackTrace =====================")
    logging.exception(ex, exc_info=True) 
    print("===================== End of Exception StackTrace =====================\n")
    message = str(ex)
    if not DEBUG:
        message = "Error processing request..."
    return HttpError(message, 500).abort()

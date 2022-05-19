from functools import wraps
from flask import jsonify
from app import db, current_user, request


class Rbac:
    user_role = ""
    user_role_pages = []
    all_role_pages = dict()

    def __init__(self, user_role):
        self.user_role = user_role.lower()
        if self.user_role in self.all_role_pages:
            self.user_role_pages = self.all_role_pages.get(self.user_role)

    def get_page_access(self, path):
        paths = path.lower().strip('/').split('/')
        page_name = paths[0]
        page_action = paths[1] if 1 < len(paths) else None
        if page_action == 'index' or page_action == None:
            page_action = 'list'
        path = f"{page_name}/{page_action}"
        return path in self.user_role_pages


# This is a custom decorator that verifies that this user has access to the page
def rbac_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        rbac = Rbac(current_user.get_role())
        path = request.path
        path = path.replace('/api/', '')
        if not rbac.get_page_access(path):
            return jsonify(f"You are not allowed to access this page '{path}'"), 403
        return fn(*args, **kwargs)
    return wrapper

from flask import request

def check_role(allowed_roles):
    role = request.headers.get("role")
    if role not in allowed_roles:
        return False
    return True
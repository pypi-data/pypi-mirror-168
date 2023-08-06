from functools import wraps

from flask import flash, redirect, url_for, abort
from flask_login import current_user

from openwebpos.blueprints.user.models import Permission


def role_required(*roles):
    """
    Check if user has permission to view this page.

    param: *roles: 1 or more allowed roles
    return: Function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role.name not in roles:
                flash("You do not have permission.", "error")
                return redirect(url_for('pos.index'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required(permission):
    """
    Check if user has permission to view this page.

    param: permission: 1 or more allowed permissions
    return: Function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def staff_required(f):
    return permission_required(Permission.STAFF)(f)

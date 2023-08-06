from datetime import datetime

from flask_login import UserMixin
from usernames import is_safe_username
from werkzeug.security import generate_password_hash, check_password_hash

from openwebpos.extensions import db
from openwebpos.utils import gen_urlsafe_token
from openwebpos.utils.sql import SQLMixin


class Permission:
    """
    Permission class for defining permissions for users.
    """
    USER = 1
    CUSTOMER = 2
    STAFF = 4
    MANAGER = 8
    ADMIN = 80


class Role(SQLMixin, db.Model):
    __tablename__ = 'roles'

    name = db.Column(db.String(100), nullable=False, unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """
        Add roles to the database.
        """
        roles = {
            'User': [Permission.USER],
            'Customer': [Permission.USER, Permission.CUSTOMER],
            'Staff': [Permission.USER, Permission.CUSTOMER, Permission.STAFF],
            'Manager': [Permission.USER, Permission.CUSTOMER, Permission.STAFF,
                        Permission.MANAGER],
            'Admin': [Permission.USER, Permission.CUSTOMER, Permission.STAFF,
                      Permission.MANAGER, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            role.save()

    def add_permission(self, perm):
        """
        Add a permission to the role.
        """
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        """
        Remove a permission from the role.
        """
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """
        Reset role permissions.
        """
        self.permissions = 0

    def has_permission(self, perm):
        """
        Check if the role has a specific permission.
        """
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


# TODO: secure user pin
class User(UserMixin, SQLMixin, db.Model):
    __tablename__ = "user"

    public_id = db.Column(db.String(25), unique=True)

    # Authentication
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(120), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(120), nullable=False, server_default='')
    pin = db.Column(db.String(120))
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')

    # Activity tracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime, nullable=True)
    current_sign_in_ip = db.Column(db.String(100), nullable=True)
    last_sign_in_at = db.Column(db.DateTime, nullable=True)
    last_sign_in_ip = db.Column(db.String(100), nullable=True)

    @staticmethod
    def insert_user():
        """
        Insert default user in the database.
        """
        Role.insert_roles()
        user = User(username='admin',
                    email='admin@mail.com',
                    password=generate_password_hash('admin'),
                    pin='1234',
                    role_id=Role.query.filter_by(name='Admin').first().id)
        user.save()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.public_id is None:
            self.public_id = gen_urlsafe_token(25)

        if self.role_id is None:
            self.role_id = Role.query.filter_by(
                name='User').first().id  # default role

    def check_password(self, password):
        return check_password_hash(password, self.password)

    def check_pin(self, pin):
        return check_password_hash(pin, self.pin)

    def check_if_safe_username(self):
        return is_safe_username(self.username)

    def is_active(self):
        """
        Return whether user account is active.
        :return: bool
        """
        return self.active

    def is_admin(self):
        """
        Return whether user is admin.
        :return: bool
        """
        return self.role_id == Role.query.filter_by(name='Admin').first().id

    def update_activity_tracking(self, ip_address: str):
        """
        Update the fields associated with user activity tracking.
        ip_address: str, IP address of the user.
        """
        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_at = datetime.utcnow()
        self.current_sign_in_ip = ip_address
        self.sign_in_count += 1

        return self.save()

    def can(self, perm):
        """
        Check if the user has a specific permission.
        """
        return self.role is not None and self.role.has_permission(perm)

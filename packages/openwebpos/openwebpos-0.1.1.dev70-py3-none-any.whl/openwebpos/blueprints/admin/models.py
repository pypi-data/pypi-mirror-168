from openwebpos.extensions import db
from openwebpos.utils.sql import SQLMixin


class Store(SQLMixin, db.Model):
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    website = db.Column(db.String(64), nullable=False)
    logo = db.Column(db.String(64), nullable=False)

    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)

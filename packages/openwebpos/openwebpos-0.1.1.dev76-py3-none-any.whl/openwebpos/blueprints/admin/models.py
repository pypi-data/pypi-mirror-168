from openwebpos.extensions import db
from openwebpos.utils.sql import SQLMixin


class Store(SQLMixin, db.Model):
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64))
    website = db.Column(db.String(64))
    logo = db.Column(db.String(64))

    printers = db.relationship('Printer', backref='store', lazy='dynamic')

    @staticmethod
    def insert_default():
        store = Store.query.first()
        if store is None:
            store = Store(name='OpenWebPOS',
                          address='123 Main Street',
                          city='City',
                          state='ST',
                          zip='12345',
                          phone='123-456-7890')
            store.save()

    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)


class Printer(SQLMixin, db.Model):
    name = db.Column(db.String(64), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(64), nullable=False, default='thermal')
    location = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False,
                         default=1)

    def __init__(self, **kwargs):
        super(Printer, self).__init__(**kwargs)

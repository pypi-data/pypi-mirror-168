import pytz
from datetime import datetime
from openwebpos.extensions import db

timezone = pytz.timezone('America/Chicago')
now = datetime.now(tz=timezone)


class SQLMixin(object):
    """
    Add the ability to save, update, and delete model instances.
    and track changes to model instances.
    """

    created_on = db.Column(db.DateTime, default=now)
    updated_on = db.Column(db.DateTime, default=now, onupdate=now)

    def save(self):
        """
        Save model instance.
        :return: model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        """
        Update model instance
        :return: db.session.commit()'s result
        """
        db.session.commit()
        return self

    def delete(self):
        """
        Delete model instance
        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

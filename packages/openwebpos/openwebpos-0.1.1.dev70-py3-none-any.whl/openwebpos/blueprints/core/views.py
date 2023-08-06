import os

from flask import Blueprint, render_template, redirect, url_for

from openwebpos.extensions import db
from openwebpos.utils import create_file
from openwebpos.blueprints.pos.models.order import OrderType, OrderPager, \
    TransactionType
from openwebpos.blueprints.user.models import User

from .forms import DatabaseConfigForm

core = Blueprint('core', __name__, template_folder='templates')


def insert_default_data() -> None:
    """
    Insert default data into the database.
    """
    # Insert default user
    User.insert_user()
    OrderType.insert_order_types()
    OrderPager.insert_order_pagers()
    TransactionType.insert_transaction_types()


@core.get('/database-config')
def database_config():
    form = DatabaseConfigForm()
    return render_template('core/database_config.html', title='Database Config',
                           form=form)


@core.get('/database-config/sqlite')
def config_sqlite_database():
    create_file(file_path=os.getcwd(),
                file_name='instance/settings.py',
                file_mode='w',
                file_content="DB_DIALECT = 'sqlite'\n")
    db.create_all()
    insert_default_data()
    return redirect(url_for('user.login'))


@core.post('/database-config/remote')
def post_config_remote_database():
    form = DatabaseConfigForm()
    if form.validate_on_submit():
        dialect = "DB_DIALECT = " + "'" + form.dialect.data + "'" + "\n"
        create_file(file_path=os.getcwd(),
                    file_name='instance/settings.py',
                    file_mode='w',
                    file_content=dialect)
        try:
            db.create_all()
        except ConnectionError():
            pass
        lines = [
            "DB_DIALECT=" + "'" + form.dialect.data + "'",
            "DB_USER=" + "'" + form.username.data + "'",
            "DB_PASS=" + "'" + form.password.data + "'",
            "DB_HOST=" + "'" + form.host.data + "'",
            "DB_PORT=" + "'" + form.port.data + "'",
            "DB_NAME=" + "'" + form.database.data + "'"
        ]
        with open(os.path.join(os.getcwd(), '.env'), 'w') as f:
            f.write('\n'.join(lines))
        return redirect('/')

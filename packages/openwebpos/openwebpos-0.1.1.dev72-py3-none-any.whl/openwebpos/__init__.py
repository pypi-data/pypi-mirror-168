import os
from importlib.metadata import version

from flask import Flask, send_from_directory, redirect, url_for

from sqlalchemy_utils import database_exists

from openwebpos.blueprints import blueprints
from openwebpos.blueprints.user.models import User
from openwebpos.extensions import db, login_manager, toolbar
from openwebpos.utils import create_folder, create_file


def open_web_pos(instance_dir=None):
    """
    Create the Flask app instance.

    Args:
        instance_dir (str): Path to the instance folder.

    Returns:
        Flask: Flask app instance.
    """
    template_dir = 'ui/templates'
    static_dir = 'ui/static'
    base_path = os.path.abspath(os.path.dirname(__file__))

    if instance_dir is None:
        instance_dir = os.path.join(os.getcwd(), 'instance')

    if os.path.isdir(instance_dir):
        if not os.listdir(instance_dir):
            create_file(file_path=os.getcwd(), file_name='instance/__init__.py')

    create_folder(folder_path=os.getcwd(), folder_name='instance')
    create_folder(folder_path=os.getcwd(), folder_name='uploads')

    app = Flask(__name__, template_folder=template_dir,
                static_folder=static_dir, instance_relative_config=True,
                instance_path=instance_dir)

    # Default settings
    app.config.from_pyfile(os.path.join(base_path, 'config/settings.py'))
    # Instance settings (overrides default settings)
    app.config.from_pyfile(os.path.join('settings.py'), silent=True)

    extensions(app)

    @app.context_processor
    def utility_processor():
        def get_package_version(package: str) -> str:
            """
            Get installed package version
            Args:
                package: String: Name of package
            Return:
                Version
            """
            return version(package)

        return dict(get_package_version=get_package_version)

    @app.route('/')
    def index():
        if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            # if User.query.count() == 0:
            #     User.insert_user()
            return redirect(url_for('pos.index'))
        return redirect(url_for('core.database_config'))

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


def extensions(app):
    """
    Register Extensions.

    Args:
        app (Flask): Flask app instance.
    """
    # from openwebpos.extensions import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # from openwebpos.blueprints.user.models import User
        return User.query.get(user_id)

    login_manager.login_view = 'user.login'

    return app

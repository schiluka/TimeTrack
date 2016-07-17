from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_filename):
    app = Flask(__name__, static_folder='templates/static')
    app.debug = True
    app.config.from_object(config_filename)

    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(
        '/Users/asraj/github/logs/timetrack.log',
        maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Init Flask-SQLAlchemy
    from app.base_model import db
    db.init_app(app)

    from app.employees.views import employees
    app.register_blueprint(employees, url_prefix='/tt/employees')

    from app.timesheets.views import timesheets
    app.register_blueprint(timesheets, url_prefix='/tt/timesheets')

    from app.base_view import login1, mail
    from flask import render_template, send_from_directory
    import os

    # Init Flask-Mail
    mail.init_app(app)

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/<path:filename>')
    def file(filename):
        return send_from_directory(
            os.path.join(app.root_path, 'templates'), filename)

    @app.route('/')
    def index():
        return render_template('index.html')

    # Auth API
    app.register_blueprint(login1, url_prefix='/tt/')

    return app

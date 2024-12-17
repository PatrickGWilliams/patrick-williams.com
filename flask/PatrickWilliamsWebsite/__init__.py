import os
from flask_mailman import Mail
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import solver

    app.register_blueprint(solver.bp)

    from . import index

    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")

    return app

from . import models

import os

from flask_mailman import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

from flask import Flask

mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config.from_pyfile("config.py")
    
    mail.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import solver

    app.register_blueprint(solver.bp)

    from . import index

    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")

    return app

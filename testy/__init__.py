
import os
from flask import Flask
from . import db, auth, novy_uzivatel, vypis_zkousek, nova_zkouska


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='david',
        DATABASE=os.path.join(app.instance_path, 'testy.db')
    )
    
    # registrace Blueprintu
    app.register_blueprint(auth.bp)
    app.register_blueprint(novy_uzivatel.bp)
    app.register_blueprint(vypis_zkousek.bp)
    app.register_blueprint(nova_zkouska.bp)
    
    app.add_url_rule('/', view_func=auth.login)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    return app
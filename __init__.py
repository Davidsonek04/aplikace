import os
from flask import Flask
from . import db, auth #, extract, create, insurance, new_insurance, create_user, update_delete


def create_app(test_config=None):
    """Vytvoří a nastaví Flask aplikaci.

    Args:
        test_config (dict, optional): Konfigurační parametry pro testování. Defaults to None.

    Returns:
        Flask: Vztvořená Flask aplikace
    """
    # Vytvoření a nastavení aplikace Flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'databaze.db'),
    )

    # registrace Blueprintů (modulů)
    app.register_blueprint(auth.bp)
    #app.register_blueprint(extract.bp)
    #app.register_blueprint(create.bp)
    #app.register_blueprint(insurance.bp)
    #app.register_blueprint(new_insurance.bp)
    #app.register_blueprint(create_user.bp)
    #app.register_blueprint(update_delete.bp)

    app.add_url_rule('/', view_func=auth.login)

    # Inicializace databáze
    db.init_app(app)

    if test_config is None:
        # načtěte konfiguraci instance, pokud existuje, když netestujete
        app.config.from_pyfile("config.py", silent=True)
    else:
        # načtěte testovací konfiguraci, pokud byla zadána
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

# end def
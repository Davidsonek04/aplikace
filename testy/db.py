import sqlite3
import click
from flask import current_app, g

def get_db():
    """Získá přístup k databázi
     
     Returns: 
        připojení k databázi
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    return g.db
# end def

def close_db(e=None):
    """Ukončuje práci s databází.

    Args:
        e: Chybový objekt, pokud existuje.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

# end def

def init_db():
    """
        Inicializuje databázi a vytvoří tabulky
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as t:
        db.executescript(t.read().decode('UTF8'))

# end def

@click.command('init-db')
def init_db_command():
    """
        Vymaže existující tabulky a vytvoří nové
    """
    init_db()
    click.echo('Inicializuji databázi')
# end def

def init_app(app):
    """Inicializuje aplikaci pro práci s databází.

    Args:
        app (Flask): Flask aplikace
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# end def
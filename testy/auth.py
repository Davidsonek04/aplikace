import functools
from flask import Blueprint, flash, g, render_template, url_for, request, session, redirect
from werkzeug.security import check_password_hash
from testy.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/')

@bp.route('/', methods= ['GET', 'POST'])
def login():
    
    # kontrola jestli uživatel existuje
    if request.method == 'POST':
        email = request.form['email']
        heslo = request.form['heslo']
        db = get_db()
        error = None
        uzivatel = db.execute(
            'SELECT * FROM uzivatele WHERE email = ?', (email,)
        ).fetchone()
        

        # ověření platnosti zadaných údajů
        if uzivatel is None or not check_password_hash(uzivatel['heslo'], heslo):
            error = f'Nesprávné přihlašovací údaje'

        if error is None:
            session.clear()
            session['email'] = uzivatel['email']

            return redirect(url_for('vypis_zkousek.vypis'))
        
        flash(error)

    return render_template('prihlaseni/prihlaseni.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@bp.before_app_request
def load_loged_in_user():
    """Načte informace o přihlášeném uživateli, pokud je přihlášen.
    Tato funkce je spuštěna před každým HTML požadavkem a zajišťuje, že informace 
    o uživateli jsou načteny do globální proměnné g.user
    """
    
    uzivatel_id = session.get('email')

    if uzivatel_id is None:
        g.user = None
    g.user = get_db().execute(
        'SELECT * FROM uzivatele WHERE email = ?', (uzivatel_id,)
    ).fetchone()

def kontrola_prihlaseni(viev):
    
    @functools.wraps(viev)
    def wraped_viev(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return viev(**kwargs)
    return wraped_viev

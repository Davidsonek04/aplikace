import functools
from flask import Blueprint, flash, g, render_template, url_for, request, session, redirect
from werkzeug.security import check_password_hash
from testy.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/')

@bp.route('/', methods= ['GET', 'POST'])
def login():
    
    # kontrola jestli uživatel existuje
    if request.method == 'POST':
        jmeno = request.form['jmeno']
        prijmeni = request.form['prijmeni']
        heslo = request.form['heslo']
        db = get_db()
        error = None
        uzivatel = db.execute(
            'SELECT * FROM uzivatele WHERE jmeno = ? AND prijmeni = ?', (jmeno, prijmeni,)
        ).fetchone()

        # ověření platnosti zadaných údajů
        if uzivatel is None or not check_password_hash(uzivatel['heslo'], heslo):
            error = f'Nesprávné přihlašovací údaje'

        if error is None:
            session.clear()
            session = uzivatel

            return redirect(url_for('vypis_zkousek.vypis'))
        
        flash(error)

    return render_template('prihlaseni/prihlaseni.html')

from flask import Blueprint, flash, g, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash
from testy.db import get_db

bp = Blueprint('/novy_uzivatel', __name__)

@bp.route('/novy_uzivatel', methods= ('GET', 'POST'))
def vytvor_uzivatele():
    if request.method == 'POST':
        jmeno = request.form['jmeno']
        email = request.form['email']
        heslo = request.form['heslo']
        db = get_db()
        error = None
        
        if (not jmeno) or (not email) or (not heslo):
            error = 'Všechny políčka jsou povinné!!!'

        test = db.execute(
            'SELECT email FROM uzivatele WHERE email = ?', (email,)
        ).fetchone()
        
        if email == test:
            error = 'Uživatel je již zaregistrovaný'

        if error is None:
            db.execute(
                'INSERT INTO uzivatele (jmeno, email, heslo) VALUES (?, ?, ?)',
                (jmeno, email, generate_password_hash(heslo),),
            )
            db.commit()
            # TODO dopsat adresu kam se má přesměrovat stránka po vytvoření uživatele
            return redirect(url_for('vypis_zkousek.vypis'))
        flash(error)
    return render_template('novy_uzivatel.html')
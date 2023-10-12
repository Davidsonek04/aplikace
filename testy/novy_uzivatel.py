
from flask import Blueprint, flash, g, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash
from testy.db import get_db

bp = Blueprint('novy_uzivatel', __name__)

@bp.route('/novy_uzivatel', methods= ('GET', 'POST'))
def vytvor_uzivatele():
    if request.method == 'POST':
        jmeno = request.form['jmeno']
        prijmeni = request.form['prijmeni']
        heslo = request.form['heslo']
        db = get_db()
        error = None
        
        if (not jmeno) or (not prijmeni) or (not heslo):
            error = f'Všechny políčka jsou povinné!!!'

        test = db.execute(
            'SELECT jmeno, prijmeni FROM uzivatele WHERE jmeno = ? AND prijmeni = ?', (jmeno, prijmeni,)
        ).fetchone()
        
        if jmeno == test['jmeno'] and prijmeni == test['prijmeni']:
            error = f'Uživatel je již zaregistrovaný'

        if error is None:
            db.execute(
                'INSERT INTO uzivatele (jmeno, prijmeni, heslo) VALUES (?, ?, ?)',
                (jmeno, prijmeni, generate_password_hash(heslo),),
            )
            db.commit()
            # TODO dopsat adresu kam se má přesměrovat stránka po vytvoření uživatele
            return redirect(url_for('vypis_zkousek.vypis'))
        flash(error)
    return render_template('novy_uzivatel.html')
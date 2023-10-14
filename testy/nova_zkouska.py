from flask import Blueprint, flash, g, render_template, redirect, request, url_for
from testy.db import get_db
from testy.auth import kontrola_prihlaseni

bp =Blueprint('nova_zkouska', __name__)

@bp.route('/nova_zkouska', methods=('GET', 'POST'))
@kontrola_prihlaseni
def nova_zkouska():
    if request.method == 'POST':
        nazev = request.form['nazev']
        pocet_otazek = request.form['pocet_otazek']
        cas = request.form['cas']

        db = get_db()
        error = None

        # Kontrola všech vyplněných políček tady zatím nebude. V případě potřeby se doplní!
        
        test = db.execute(
            'SELECT nazev FROM typ_zkousky WHERE nazev = ?', (nazev,)
        ).fetchone()

        # Kontrola jestli typ zkoušky existuje
        if test is not None:
            error = "Tento typ zkoušky je už zaveden!"

        if error is None:
            db.execute(
                'INSERT INTO typ_zkousky (nazev, pocet_otazek, cas) VALUES (?, ?, ?)', (nazev, pocet_otazek, cas,),
            )
            db.commit()
            error = "Zkouška byla vytvořena"
            flash(error)
            return redirect(url_for('vypis_zkousek.vypis'))
        flash(error)
    return render_template('nova_zkouska.html')
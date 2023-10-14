
from flask import Blueprint, render_template
from testy.auth import kontrola_prihlaseni
from testy.db import get_db

bp = Blueprint('vypis_zkousek', __name__)

@bp.route('/vypis_zkousek', methods= ('GET', 'POST'))
@kontrola_prihlaseni
def vypis():
    """Zobrazí seznam a typ odborných zkoušek
    """
    db = get_db()

    zkousky = db.execute(
        'SELECT * FROM typ_zkousky'
    ).fetchall()
    return render_template('/vypis_zkousek.html', zkousky=zkousky)
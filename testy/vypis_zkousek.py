
from flask import Blueprint, render_template
from testy.auth import login_required
from testy.db import get_db

bp = Blueprint('zkousky', __name__)

@bp.route('/vypis_zkousek', methods= ('GET', 'POST'))
@login_required
def vypis():
    """Zobrazí seznam a typ odborných zkoušek
    """
    db = get_db()

    zkousky = db.execute(
        'SELECK * FROM typ_zkousky'
    ).fetchall()
    return render_template('zkousky/vypis_zkousek.html', zkousky=zkousky)
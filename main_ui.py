from flask import (
    Blueprint, render_template
)

from bme280_sensor import bme280_date
from .db import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    db_data = db.execute(
        'SELECT *'
        ' FROM bme280'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('index.html', db_data=db_data)


def update():
    db = get_db()
    _bme280 = bme280_date(2)

    while True:
        t, h, p = next(_bme280)
        db.execute(
            'INSERT INTO bme280 (temperature, humidity, pressure)'
            ' VALUES (?, ?, ?)',
            (t, h, p,)
        )
        db.commit()
    # return render_template('index.html')

from flask import (
    Blueprint, render_template
)

from .db import get_db

bp = Blueprint('sensors', __name__)
db_data = []


@bp.route('/sensors')
def index():
    global db_data
    db = get_db()
    db_data = db.execute(
        'SELECT *'
        ' FROM bme280'
        ' ORDER BY created DESC LIMIT 20'
    ).fetchall()
    return render_template('sensors/sensors.html', db_data=db_data)


@bp.route('/sensors/temp_bme280')
def show_tem_bme280():
    return render_template('sensors/temp_bme280.html', db_data=db_data)


@bp.route('/sensors/hum_bme280')
def show_hum_bme280():
    return render_template('sensors/hum_bme280.html', db_data=reversed(db_data))

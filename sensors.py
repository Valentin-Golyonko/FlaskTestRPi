from flask import (
    Blueprint, render_template)

from color_log.log_color import *
from db import get_db, close_db
from rpi_temp import measure_rpi_temp

bp = Blueprint('sensors', __name__)


@bp.route('/sensors')
def index():
    log_verbose("sensors: index()")
    global db_data, _id, t, h, p, c, rp
    cur = get_db().cursor()
    db_data = cur.execute(
        'SELECT *'
        ' FROM bme280'
        ' ORDER BY created DESC LIMIT 50'
    ).fetchall()
    close_db()

    _id = [i['id'] for i in db_data]
    t = [i['temperature'] for i in db_data]
    h = [i['humidity'] for i in db_data]
    p = [i['pressure'] for i in db_data]
    c = [i['created'].strftime('%x %X') for i in db_data]
    # log_info("\tcreated: %s %s" % (c, type(c[0])))

    rpi_temp = measure_rpi_temp(2)
    rp = next(rpi_temp)

    return render_template('sensors/sensors.html', db_data=[db_data, _id, t, h, p, c, rp])
    # return redirect(url_for('sensors.index'))


@bp.route('/sensors/temp_bme280')
def show_tem_bme280():
    log_verbose("sensors: show_tem_bme280()")
    return render_template('sensors/temp_bme280.html', db_data=[db_data, _id, t, h, p, c, rp])


@bp.route('/sensors/hum_bme280')
def show_hum_bme280():
    log_verbose("sensors: show_hum_bme280()")
    return render_template('sensors/hum_bme280.html', db_data=[reversed(db_data), _id, t, h, p, c, rp])

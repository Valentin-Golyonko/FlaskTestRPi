from flask import (
    Blueprint, render_template, request, redirect, url_for, flash)

from .color_log.log_color import log_verbose, log_info, log_warning
from .db import get_db, close_db
from .rpi_temp import measure_rpi_temp

bp = Blueprint('smart_home', __name__)


@bp.route('/smart_home')
def index():
    log_verbose("smart_home: index()")
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

    rpi_temp = measure_rpi_temp(2)
    rp = next(rpi_temp)

    return render_template('smart_home/smart_home.html', db_data=[db_data, _id, t, h, p, c, rp])
    # return redirect(url_for('smart_home.index'))


@bp.route('/smart_home/create', methods=("GET", "POST"))
def create():
    log_verbose("smart_home/create()")
    if request.method == 'POST':
        s_name = request.form['s_name']
        s_address = request.form['s_address']
        check_tmp = request.form.get('check_tmp')
        check_hum = request.form.get('check_hum')
        check_air = request.form.get('check_air')
        check_press = request.form.get('check_press')
        s_else = request.form['s_else']
        check_else = request.form.get('check_else')
        error = None

        log_warning("n %s, a %s, t %s, h %s, a %s, p %s, e %s %s" % (
            s_name, s_address, check_tmp, check_hum, check_air, check_press, s_else, check_else))

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()
            pass
            db.commit()
            close_db()

        return redirect(url_for('smart_home.index'))

    return render_template('smart_home/create.html')

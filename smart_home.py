from flask import (
    Blueprint, render_template, request, redirect, url_for)

from color_log.log_color import log_verbose, log_warning
from db import get_db, close_db
from rpi_temp import measure_rpi_temp

bp = Blueprint('smart_home', __name__)


@bp.route('/smart_home')
def index():
    log_verbose("smart_home: index()")

    cur = get_db().cursor()

    # --- bme280 ---------------------------------------------------------------------
    db_data = cur.execute(
        'SELECT *'
        ' FROM bme280'
        ' ORDER BY created DESC LIMIT 50'
    ).fetchall()

    _id = [i['id'] for i in db_data]
    t = [i['temperature'] for i in db_data]
    h = [i['humidity'] for i in db_data]
    p = [i['pressure'] for i in db_data]
    c = [i['created'].strftime('%x %X') for i in db_data]

    # --- rpi cpu ---------------------------------------------------------------------
    rpi_temp = measure_rpi_temp(2)
    rp = next(rpi_temp)

    # --- more home iot ---------------------------------------------------------------
    db_iot_names = cur.execute('SELECT iot_name FROM home_iot').fetchall()
    db_iot_names = [i[0] for i in db_iot_names]

    db_iot_data = []  # crutch !
    if db_iot_names:
        for name in db_iot_names:
            db_iot_data_i = cur.execute(
                f'SELECT temp, hum, air, press, TEXT, created '
                f'FROM {name} '
                f'ORDER BY created '
                f'DESC LIMIT 50'
            ).fetchall()
            t_iot = [i['temp'] for i in db_iot_data_i]
            h_iot = [i['hum'] for i in db_iot_data_i]
            a_iot = [i['air'] for i in db_iot_data_i]
            p_iot = [i['press'] for i in db_iot_data_i]
            # test_iot = [i[4] for i in db_iot_data_i]
            c_iot = [i['created'].strftime('%x %X') for i in db_iot_data_i]

            db_iot_data.append([t_iot, h_iot, a_iot, p_iot, c_iot])

        # log_warning("db_iot_data_i: %s" % db_iot_data)

    # --- close DB ---------------------------------------------------------------------
    close_db()

    return render_template('smart_home/smart_home.html',
                           db_data=[db_data, _id, t, h, p, c, rp, db_iot_names, db_iot_data])
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
        s_description = request.form['s_description']

        log_warning("n %s, a %s, t %s, h %s, a %s, p %s, e %s %s, d %s" % (
            s_name, s_address, check_tmp, check_hum, check_air, check_press, s_else, check_else, s_description))

        if str(s_name).isalnum():
            db = get_db()
            cur = db.cursor()

            cur.execute("INSERT INTO home_iot"
                        " (iot_name, iot_address, iot_description)"
                        " VALUES (?, ?, ?)",
                        [s_name, s_address, s_description])
            db.commit()

            cur.execute(f"CREATE TABLE IF NOT EXISTS {s_name}"
                        f" (temp NUMERIC,"
                        f" hum NUMERIC,"
                        f" air NUMERIC,"
                        f" press NUMERIC,"
                        f" {s_else} TEXT,"
                        f" created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
                        f";")
            db.commit()

            close_db()

            return redirect(url_for('smart_home.index'))

    return render_template('smart_home/create.html')

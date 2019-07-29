from flask import Blueprint, render_template

from color_log.log_color import log_verbose

bp = Blueprint('calendar', __name__, template_folder='templates')


@bp.route('/calendar')
def index():
    log_verbose("calendar: index()")
    return render_template('calendar/calendar_main.html')

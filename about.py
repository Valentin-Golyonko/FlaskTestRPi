from flask import (
    Blueprint, render_template)

from color_log.log_color import log_verbose

bp = Blueprint('about', __name__)


@bp.route('/about')
def index():
    log_verbose("about: index()")
    return render_template('about.html')

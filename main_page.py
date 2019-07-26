from flask import Blueprint, render_template

from color_log.log_color import log_verbose

bp = Blueprint('main', __name__, template_folder='templates')


@bp.route('/')
def index():
    log_verbose("main page()")
    return render_template('main_page.html')

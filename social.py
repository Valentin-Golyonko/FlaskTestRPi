from flask import (
    Blueprint, render_template)

bp = Blueprint('social', __name__)


@bp.route('/social', methods=('GET', 'POST'))
def index():
    return render_template('social/social.html')

from flask import (Blueprint, render_template, redirect, url_for)

from Twee import twee
from color_log.log_color import log_info, log_error
from work_with_twee_db import create_db_twee_table, log_verbose

bp = Blueprint('social', __name__)


@bp.route('/social', methods=('GET', 'POST'))
def index():
    log_verbose("social.index()")

    # feed_from_db = open_db_twee_table()
    feed_from_db = twee()  # TODO: Streaming https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/

    if feed_from_db:
        log_info("\tfeed_from_db - OK")
        return render_template('social/social.html', data=feed_from_db)
    else:
        log_error("\tfeed_from_db - None")
        return redirect(url_for('social'))


def save_feed():
    log_verbose("save_feed()")

    feed = twee()

    if feed:
        log_info("\tload_feed - OK")
    else:
        log_error("\tload_feed = None")

    ok = create_db_twee_table(feed)

    if ok:
        log_info("\tsave_feed - OK")
    else:
        log_error("\tsave_feed = None")

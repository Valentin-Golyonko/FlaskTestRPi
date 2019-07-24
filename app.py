import os
from threading import Thread

from flask import Flask

import about
import db
import main_page
import smart_home
import social
import weather
from bme280_sensor import update_bme280_db_table

# def create_app(test_config=None):
from one_more_home_iot import my_server

"""Create and configure an instance of the Flask application."""
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY='dev',
    # store the database in the instance folder
    DATABASE=os.path.join(app.root_path, 'data/flask_test.sqlite'),
)

# if test_config is None:
# load the instance config, if it exists, when not testing
# app.config.from_pyfile('config.py', silent=True)
# else:
# load the test config if passed in
# app.config.update(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.route('/hello')
def hello():
    return 'Hello, World!'


# register the database commands
db.init_app(app)

# apply the blueprints to the app

app.register_blueprint(main_page.bp)

app.register_blueprint(smart_home.bp)

app.register_blueprint(weather.bp)

app.register_blueprint(social.bp)

app.register_blueprint(about.bp)

th_s = Thread(target=update_bme280_db_table, daemon=True, name="Thread - update_bme280_db_table")
th_s.start()

# from .weather import update_owm_db_table
# th_w = Thread(target=update_owm_db_table, daemon=True, name="Thread - update_owm_db_table")
# th_w.start()

# my_server()

# make url_for('index') == url_for('blog.index')
# in another app, you might define a separate main index here with
# app.route, while giving the blog blueprint a url_prefix, but for
# the tutorial the blog will be the main index
app.add_url_rule('/', endpoint='home')

# return app


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

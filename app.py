import os

from flask import Flask
from threading import Thread


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.root_path, 'flask_test.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the database commands
    from db import init_app
    init_app(app)

    # apply the blueprints to the app
    from . import main
    app.register_blueprint(main.bp)

    from . import sensors
    app.register_blueprint(sensors.bp)

    #
    from bme280_sensor import update_db
    th_s = Thread(target=update_db, daemon=True, name="upd_bme280")
    th_s.start()

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='home')

    return app

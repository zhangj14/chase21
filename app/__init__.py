import os
from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect

def create_app(test_config=None):
    # create and config the program
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, '')
    )

    if test_config == None:
        # load the instance config when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exist
    try:
        os.makedirs(app.instance_path)
    except:
        pass

    @app.route("/")
    def index():
        return redirect(url_for("info.index"))

    from . import db
    db.init_app(app)

    from . import admin
    admin.init_app(app)

    from . import emailing
    emailing.init_app(app)

    from . import info
    app.register_blueprint(info.bp)

    from . import forms
    app.register_blueprint(forms.bp)

   
    return app
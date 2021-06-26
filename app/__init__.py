import os
import secrets

from flask import Flask
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
		FLASK_APP='app:name',
        SECRET_KEY='dev',
		FLASK_ENV='development',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
		OAUTHLIB_INSECURE_TRANSPORT='1'
    )
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = secrets.token_hex(16)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    github_blueprint = make_github_blueprint(
        client_id="bad4ab0afbd8cb1be0a5",
        client_secret="badb4088cffa7efcd2b589225188fad755db53",
    )
    app.register_blueprint(github_blueprint, url_prefix='/login')

    google_blueprint = make_google_blueprint(
        client_id="bad-mihp07r48ievl44loe3uepqt9dtq4hs7.apps.googleusercontent.com",
        client_secret="bad4q2PJ5gYrKdt1uVmiVfVbj",
        scope=["openid"]
    )
    app.register_blueprint(google_blueprint, url_prefix="/login")

    from . import pages
    app.register_blueprint(pages.bp)

    from . import guest
    app.register_blueprint(guest.bp)


    return app
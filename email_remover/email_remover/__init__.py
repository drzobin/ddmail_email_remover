import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    """Create and configure an instance of the Flask application email_remover."""
    app = Flask(__name__, instance_relative_config=True)

    # Set app configurations from configuration file config.py
    mode=os.environ.get('MODE')
    if mode == "PRODUCTION":
        app.config.from_object("config.Prod")
    elif mode == "TESTING":
        app.config.from_object("config.Test")
    elif mode == "DEVELOPMENT":
        app.config.from_object("config.Dev")
    else:
        print("Error: you need to set env variabel MODE to PRODUCTION/TESTING/DEVELOPMENT")
        exit(1)
    
    app.secret_key = app.config["SECRET_KEY"]
    app.WTF_CSRF_SECRET_KEY = app.config["WTF_CSRF_SECRET_KEY"]
    csrf = CSRFProtect(app)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Apply the blueprints to the app
    from email_remover import application
    app.register_blueprint(application.bp)

    return app 

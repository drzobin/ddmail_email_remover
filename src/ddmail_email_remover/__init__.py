import os
import sys
import toml
from flask import Flask
import logging
from logging.config import dictConfig
from logging import FileHandler


def create_app(config_file=None, test_config=None):
    """
    Create and configure an instance of the Flask application ddmail_email_remover.
    
    This function is the application factory for the ddmail_email_remover application.
    It sets up logging, loads configuration from a TOML file, configures the application
    based on the current mode (PRODUCTION/TESTING/DEVELOPMENT), and registers blueprints.
    
    Args:
        config_file (str, optional): Path to the TOML configuration file. Required for application to start.
        test_config (dict, optional): Test configuration dictionary that can override the default configuration.
                                     Not currently used but available for future test customization.
    
    Returns:
        Flask: A configured Flask application instance.
    
    Raises:
        SystemExit: If config_file is not provided or if MODE environment variable is not set correctly.
    
    Environment Variables:
        MODE: Must be set to one of 'PRODUCTION', 'TESTING', or 'DEVELOPMENT' to determine which
              configuration section to use from the config file.
    
    Configuration File Structure (TOML):
        The configuration file should contain sections for each mode with the following keys:
        - SECRET_KEY: Used for securely signing session cookies and other security needs
        - PASSWORD_HASH: Hashed password for authentication
        - EMAIL_ACCOUNT_PATH: Path to the email accounts directory
        - LOGFILE: Path to the log file for this mode
    """

    # Configure base logging to stream handler for console output
    # This sets up the initial logging configuration for the application
    # with a standardized format that includes timestamp, level, module, function, and line number
    log_format = '[%(asctime)s] %(levelname)s in %(module)s %(funcName)s %(lineno)s: %(message)s'
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': log_format
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    # Create the Flask application instance with instance_relative_config=True
    # This tells Flask that configuration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)

    toml_config = None

    # Validate that a configuration file was provided
    # The application requires a TOML configuration file to operate
    if config_file is None:
        print("Error: you need to set path to configuration file in toml format")
        sys.exit(1)

    # Load and parse the TOML configuration file
    # This file contains all the environment-specific settings
    with open(config_file, 'r') as f:
        toml_config = toml.load(f)

    # Determine which configuration section to use based on the MODE environment variable
    # This allows for different configurations in production, testing, and development
    mode = os.environ.get('MODE')
    print("Running in MODE: " + str(mode))
    if mode == "PRODUCTION":
        # Load production configuration settings
        app.config["SECRET_KEY"] = toml_config["PRODUCTION"]["SECRET_KEY"]
        app.config["PASSWORD_HASH"] = toml_config["PRODUCTION"]["PASSWORD_HASH"]
        app.config["EMAIL_ACCOUNT_PATH"] = toml_config["PRODUCTION"]["EMAIL_ACCOUNT_PATH"]

        # Set up file-based logging for production environment
        # This logs to a specified file path rather than just the console
        file_handler = FileHandler(filename=toml_config["PRODUCTION"]["LOGFILE"])
        file_handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(file_handler)
    elif mode == "TESTING":
        # Load testing configuration settings
        app.config["SECRET_KEY"] = toml_config["TESTING"]["SECRET_KEY"]
        app.config["PASSWORD_HASH"] = toml_config["TESTING"]["PASSWORD_HASH"]
        app.config["EMAIL_ACCOUNT_PATH"] = toml_config["TESTING"]["EMAIL_ACCOUNT_PATH"]

        # Set up file-based logging for testing environment
        file_handler = FileHandler(filename=toml_config["TESTING"]["LOGFILE"])
        file_handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(file_handler)
    elif mode == "DEVELOPMENT":
        # Load development configuration settings
        app.config["SECRET_KEY"] = toml_config["DEVELOPMENT"]["SECRET_KEY"]
        app.config["PASSWORD_HASH"] = toml_config["DEVELOPMENT"]["PASSWORD_HASH"]
        app.config["EMAIL_ACCOUNT_PATH"] = toml_config["DEVELOPMENT"]["EMAIL_ACCOUNT_PATH"]

        # Set up file-based logging for development environment
        file_handler = FileHandler(filename=toml_config["DEVELOPMENT"]["LOGFILE"])
        file_handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(file_handler)
    else:
        # Exit if the MODE environment variable is not set to a recognized value
        print("Error: you need to set env variabel MODE to PRODUCTION/TESTING/DEVELOPMENT")
        sys.exit(1)

    # Set the Flask secret key from the loaded configuration
    # This is used for signing sessions and securing cookies
    app.secret_key = app.config["SECRET_KEY"]

    # Create the instance folder if it doesn't exist
    # This is where Flask will store instance-specific data
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Ignore the error if the directory already exists
        pass

    # Register the application blueprint that contains the routes
    # This modularizes the application into separate components
    from ddmail_email_remover import application
    app.register_blueprint(application.bp)

    # Return the configured Flask application
    return app

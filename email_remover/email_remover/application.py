from flask import Blueprint, current_app, request
from argon2 import PasswordHasher
import os
import shutil
import time
import logging

from email_remover.validators import is_domain_allowed, is_password_allowed, is_email_allowed

bp = Blueprint("application", __name__, url_prefix="/")

# Configure logging.
logging.basicConfig(filename="/var/log/ddmail_email_remover.log", format='%(asctime)s: %(levelname)s: %(message)s', level=logging.ERROR)

@bp.route("/hash_data", methods=["POST"])
def hash_data():
    if request.method == 'POST':
        ph = PasswordHasher()

        data = request.form.get('data')

        # Validate password.
        if is_password_allowed(data) != True:
            logging.error("hash_data() password validation failed")
            return "error: password validation failed"

        data_hash = ph.hash(data)

        return data_hash

@bp.route("/", methods=["POST"])
def main():
    if request.method == 'POST':
        ph = PasswordHasher()

        password = request.form.get('password')
        domain = request.form.get('domain')
        email = request.form.get('email')

        # Validate password.
        if is_password_allowed(password) != True:
            logging.error("main() password validation failed")
            return "error: password validation failed"

        # Validate domain.
        if is_domain_allowed(domain) != True:
            logging.error("main() domain validation failed")
            return "error: domain validation failed"

        # Validate email.
        if is_email_allowed(email) != True:
            logging.error("main() domain validation failed")
            return "error: email validation failed"

        # Check if password is correct.
        try:
            if ph.verify(current_app.config["PASSWORD_HASH"], password) != True:
                time.sleep(1)
                logging.error("main() wrong password")
                return "error: wrong password"
        except:
            time.sleep(1)
            logging.error("main() wrong password")
            return "error: wrong password"
        time.sleep(1)

        # Split email and verify domain.
        splitted_email_domain = email.split('@')
        if splitted_email_domain[1] != domain:
            logging.error("main() email address domain do no match domain")
            return "error: email adress domain do not match domain"

        # Path to email folder on disc.
        email_path = current_app.config["EMAIL_ACCOUNT_PATH"] + "/" + domain + "/" + splitted_email_domain[0]

        # Check if email folder excist.
        if os.path.isdir(email_path) != True:
            logging.error("main() email account folder do not excist")
            return "error: email account folder do not excist"
    
        # location of rm binary.
        rm = "/usr/bin/rm"

        # Check that rm exist.
        if os.path.exists(rm) != True:
            logging.error("main() rm binary location is wrong")
            return "error: rm binary location is wrong"

        # Remove email folder from hdd.
        try:
            output = subprocess.run(["/usr/bin/doas",rm,"-rf",email_path], check=True)
            if output.returncode != 0:
                logging.error("main() returncode of cmd rm is non zero")
                return "error: returncode of cmd rm is non zero"
        except subprocess.CalledProcessError as e:
            logging.error("main() returncode of cmd rm is non zero")
            return "error: returncode of cmd rm is non zero"
        except:
            logging.error("main() unkonwn exception running subprocess")
            return "error: unkonwn exception running subprocess"

        logging.debug("main() done")
        return "done"

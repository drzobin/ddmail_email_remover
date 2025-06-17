import os
import time
import subprocess
from flask import Blueprint, current_app, request, make_response, Response
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import ddmail_validators.validators as validators

bp = Blueprint("application", __name__, url_prefix="/")

@bp.route("/", methods=["POST"])
def main() -> Response:
    if request.method != 'POST':
        return make_response("Method not allowed", 405)
        
    ph = PasswordHasher()
    
    password = request.form.get('password')
    domain = request.form.get('domain')
    email = request.form.get('email')

    # Check if input from form is None.
    if password is None:
        current_app.logger.error("password is None")
        return make_response("error: password is none", 200)

    if domain is None:
        current_app.logger.error("domain is None")
        return make_response("error: domain is none", 200)

    if email is None:
        current_app.logger.error("email is None")
        return make_response("error: email is none", 200)

    # Validate password.
    if validators.is_password_allowed(password) is not True:
        current_app.logger.error("password validation failed")
        return make_response("error: password validation failed", 200)

    # Validate domain.
    if validators.is_domain_allowed(domain) is not True:
        current_app.logger.error("domain validation failed")
        return make_response("error: domain validation failed", 200)

    # Validate email.
    if validators.is_email_allowed(email) is not True:
        current_app.logger.error("domain validation failed")
        return make_response("error: email validation failed", 200)

    # Check if password is correct.
    try:
        if ph.verify(current_app.config["PASSWORD_HASH"], password) is not True:
            time.sleep(1)
            current_app.logger.error("wrong password")
            return make_response("error: wrong password", 200)
    except VerifyMismatchError:
        time.sleep(1)
        current_app.logger.error("VerifyMismatchError, wrong password")
        return make_response("error: wrong password", 200)
    time.sleep(1)

    # Split email and verify domain.
    splitted_email_domain = email.split('@')
    if splitted_email_domain[1] != domain:
        current_app.logger.error("email address domain do no match domain")
        return make_response("error: email adress domain do not match domain", 200)

    # Path to email folder on disc.
    email_path = current_app.config["EMAIL_ACCOUNT_PATH"] + "/" + domain + "/" + splitted_email_domain[0]

    # location of rm binary.
    rm = "/usr/bin/rm"

    # Check that rm exist.
    if os.path.exists(rm) is not True:
        current_app.logger.error("rm binary location is wrong")
        return make_response("error: rm binary location is wrong", 200)

    # Remove email folder from hdd.
    try:
        output = subprocess.run(
                ["/usr/bin/doas", "-u", "vmail", rm, "-rf", email_path],
                check=True
                )
        if output.returncode != 0:
            current_app.logger.error("returncode of cmd rm is non zero")
            return make_response("error: returncode of cmd rm is non zero", 200)
    except subprocess.CalledProcessError:
        current_app.logger.error("returncode of cmd rm is non zero")
        return make_response("error: returncode of cmd rm is non zero", 200)

    current_app.logger.info("done")
    return make_response("done", 200)

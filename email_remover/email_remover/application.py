from flask import Blueprint, session, render_template, current_app, request
from argon2 import PasswordHasher
import os
import shutil

from email_remover.validators import is_domain_allowed, is_password_allowed, is_email_allowed

bp = Blueprint("application", __name__, url_prefix="/")

@bp.route("/", methods=["POST"])
def main():
    if request.method == 'POST':
        ph = PasswordHasher()

        password = request.form.get('password')
        domain = request.form.get('domain')
        email = request.form.get('email')

        # Validate password.
        if is_password_allowed(password) != True:
            return "done"

        # Validate domain.
        if is_domain_allowed(domain) != True:
            return "done"

        # Validate email.
        if is_email_allowed(email) != True:
            return "done"

        # Check if password is correct.
        try:
            if ph.verify(current_app.config["PASSWORD_HASH"], cleartext_password) != True:
                print("Wrong password")
                return "done"
        except:
            print("Wrong password")
            return "done"

        # Path to email folder on disc.
        email_path = current_app.config["EMAIL_ACCOUNT_PATH"] + "/" + domain + "/" + email

        # Check if email folder exsist.
        if os.path.isdir(email_path) != True:
            return "done"

        # Remove email folder from hdd.
        shutil.rmtree(email_path)

    return "done"

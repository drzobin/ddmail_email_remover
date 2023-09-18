from flask import Blueprint, session, render_template

bp = Blueprint("application", __name__, url_prefix="/")

@bp.route("/")
def main():

    return "main"

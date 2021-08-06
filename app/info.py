import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('info', __name__)

@bp.route("/")
@bp.route("/index")
@bp.route("/home")
def index():
    return render_template('info/index2.html')

@bp.route("/contact/")
def contact():
    return render_template('info/contact.html')

@bp.route("/current_game/")
def current_game():
    return render_template('info/scores.html')
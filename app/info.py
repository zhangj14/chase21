from .db import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('info', __name__)

@bp.route("/")
@bp.route("/index")
@bp.route("/home")
def index():
    return render_template('info/index.html')

@bp.route("/contact/")
def contact():
    return render_template('info/contact.html')

@bp.route("/current_game/")
def current_game():
    db, cursor = get_db(dict=False)
    cursor.execute("SELECT fname, lname, form, CONCAT('Year ', year_level), house, caught_count, game_status FROM all_players WHERE game_status <> 'opt_out'")
    headers = ("First name","Last name", "Form class", "Year level", "House", "Score", "Game status")
    data = cursor.fetchall()
    return render_template('info/scores.html', headers=headers, data=data)
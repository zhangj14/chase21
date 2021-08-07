from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request
)

from .db import get_db

bp = Blueprint("forms", __name__, url_prefix="/forms")

@bp.route("/")
def forms():
    return render_template("forms/all_forms.html")

@bp.route("/caught", methods=["GET", "POST"])
def caught():
    if request.method == "POST":
        # get form values
        chaser_id = request.form["chaser_id"]
        runner_id = request.form['runner_id']
        valid = False
        # get db connection
        cnx, cursor = get_db()
        message = None
        # exceptions
        if not chaser_id:
            message = "Chaser ID is required."
        elif not runner_id:
            message = "Runner ID is required."
        else:
            cursor.execute(f"SELECT runner_id FROM all_players WHERE chaser_id = '{chaser_id}'")
            try:
                # check runner_id
                if cursor.fetchone()['runner_id'] != runner_id:
                    message = "Please double check your Chaser ID and Runner ID."
            # if cursor return none type then chaser id is invalid
            except TypeError:
                message = "Invalid Chaser ID."
        if message is None:
            cursor.execute(f"UPDATE all_players SET game_status = 'dead' WHERE chaser_id = '{runner_id}'")
            cursor.execute(f"UPDATE all_players SET caught_count = caught_count + 1 WHERE chaser_id = '{chaser_id}'")
            message = "Congratulations!"
            valid = True
        cursor.execute("INSERT INTO caught (chaser_id, runner_id, valid) values (%s, %s, %s)", (chaser_id, runner_id, valid))
        cnx.commit()
        flash(message)
    return render_template("forms/caught.html")

@bp.route("/opt_out", methods=["GET", "POST"])
def opt_out():
    if request.method == "POST":
        # get form values
        email = request.form['email']
        reasons = request.form['reasons']
        valid = False
        # get db connection
        cnx, cursor = get_db()
        message = None
        # exceptions
        if not email:
            message = "Your email adress is required."
        else:
            cursor.execute(f"SELECT game_status FROM all_players WHERE email = '{email}'")
            player = cursor.fetchone()
            if not player:
                message = "Invalid email."
            elif player['game_status'] == 'opt_out':
                message = "You have opt out already!"
        if message is None:
            cursor.execute(f"UPDATE all_players SET game_status = 'opt_out' WHERE email = '{email}'")
            message = "Sorry to see you go!"
            valid = True
        cursor.execute("INSERT INTO opt_out (email, reasons, valid) values (%s, %s, %s)", (email, reasons, valid))
        cnx.commit()
        flash(message)
    return render_template("forms/opt_out.html")

@bp.route("/reassign", methods=["GET", "POST"])
def reassign():
    if request.method == "POST":
        # get form values
        chaser_id = request.form["chaser_id"]
        fname = request.form['fname']
        valid = False
        # get db connection
        cnx, cursor = get_db()
        message = None
        # exceptions
        if not chaser_id:
            message = "Chaser ID is required."
        elif not fname:
            message = "Your first name is required."
        else:
            cursor.execute(f"SELECT fname, runner_id, house, year_level FROM all_players WHERE chaser_id = '{chaser_id}'")
            chaser = cursor.fetchone()
            try:
                # check runner_id
                if chaser['fname'] != fname:
                    message = "Please double check your Chaser ID and first name."
            # if cursor return none type then chaser id is invalid
            except TypeError:
                message = "Invalid Chaser ID."
        if message is None:
            # update original runner's status
            cursor.execute(f"UPDATE all_players SET game_status = 'absent', chaser_count = chaser_count - 1 WHERE chaser_id = '{chaser['runner_id']}'")
            # select potential new runners
            cursor.execute(f"SELECT chaser_id FROM all_players WHERE house <> '{chaser['house']}' AND year_level = {chaser['year_level']} AND game_status = 'alive' ORDER BY chaser_count LIMIT 1")
            new_runners = cursor.fetchone()
            # update chaser's information
            cursor.execute(f"UPDATE all_players SET runner_id = '{new_runners['chaser_id']}', reassign_count = reassign_count + 1 WHERE chaser_id = '{chaser_id}'")
            # update new runner's information
            cursor.execute(f"UPDATE all_players SET chaser_count = chaser_count + 1 WHERE chaser_id = '{new_runners['chaser_id']}'")
            message = "Successful."
            valid = True
        cursor.execute("INSERT INTO reassign (chaser_id, fname, valid) values (%s, %s, %s)", (chaser_id, fname, valid))
        cnx.commit()
        flash(message)
    return render_template("forms/reassign.html")

@bp.route("/report", methods=["GET", "POST"])
def report():
    return render_template("forms/report.html")
from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request
)

from app.db import get_db

bp = Blueprint("forms", __name__, url_prefix="/forms")

@bp.route("/")
def forms():
    return render_template("forms/all_forms.html")

@bp.route("/caught", methods=("GET", "POST"))
def caught():
    if request.method == "POST":
        chaser_id = request.form['chaser_id']
        runner_id = request.form['runner_id']
        valid = False
        db, cursor = get_db() # get database connection
        message = None

        if not chaser_id:
            message = "Chaser ID is required."
        elif not runner_id:
            message = "Runner ID is required."
        else:
            # select the person's runner_id with corresponding chaser_id
            cursor.execute(f"SELECT runner_id FROM all_players \
                            WHERE chaser_id = '{chaser_id}' LIMIT 1")
            db_runner_id = cursor.fetchone()

        if not db_runner_id:
            message = "Invalid chaser ID."
        elif db_runner_id[0] != runner_id:
            message = "Please double check your Chaser ID and Runner ID."
        if message is None:
            valid = True
            cursor.execute(f"UPDATE all_players SET game_status = 'dead' \
                            WHERE chaser_id = '{runner_id}'")
            message = "Congratulations on catching your runner."
        cursor.execute(f"INSERT INTO caught (chaser_id, runner_id, valid) \
                    values ('{chaser_id}', '{runner_id}', {valid})")
        db.commit()
        flash(message)
    return render_template("forms/caught.html")

@bp.route("/opt_out", methods=("GET", "POST"))
def op_out():
    if request.method == "POST":
        email = request.form["email"]
        reasons = request.form["reasons"]
        db = get_db().cursor()
        db.execute(f"INSERT INTO opt_out (email, reasons) VALUES ({email}, {reasons})")
    return render_template("forms/opt_out.html")

@bp.route("/reassign", methods=("GET", "POST"))
def reassign():
    return render_template("forms/reassign.html")

@bp.route("/report", methods=("GET", "POST"))
def report():
    return render_template("forms/report.html")
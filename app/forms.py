from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request
)

from .db import *

bp = Blueprint("forms", __name__, url_prefix="/forms")

@bp.route("/")
def forms():
    return render_template("forms/all_forms.html")

@bp.route("/caught", methods=["GET", "POST"])
def caught():
    if request.method == "POST":
        chaser_id = request.form["chaser_id"]
        runner_id = request.form['runner_id']
        valid = True
        db = get_db().cursor()
        error = None
        if not chaser_id:
            error = "Chaser ID is required."
        elif not runner_id:
            error = "Runner ID is required"
        else:
            db.execute(f"SELECT runner_id FROM all_players \
                       WHERE chaser_id = '{chaser_id}' LIMIT 1")
            if db.fetchone() != runner_id:
                valid = False
                error = "Please double check your Chaser ID and Runner ID."
            db.execute(f"INSERT INTO caught (chaser_id, runner_id, valid) \
                       values ('{chaser_id}', '{runner_id}', {valid})")
        if error is None:
            db.execute(f"UPDATE all_players SET game_status = 'dead' \
                       WHERE chaser_id = {runner_id}")
    return render_template("forms/caught.html")

@bp.route("/opt_out", methods=["GET", "POST"])
def op_out():
    if request.method == "POST":
        email = request.form["email"]
        reasons = request.form["reasons"]
        db = get_db().cursor()
        db.execute(f"INSERT INTO opt_out (email, reasons) VALUES ({email}, {reasons})")
    return render_template("forms/opt_out.html")

@bp.route("/reassign", methods=["GET", "POST"])
def reassign():
    return render_template("forms/reassign.html")

@bp.route("/report", methods=["GET", "POST"])
def report():
    return render_template("forms/report.html")
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
        year_level = request.form['year_level']
        valid = True
        db = get_db().cursor()
        error = None
        if not chaser_id:
            error = "Chaser ID is required."
        elif not runner_id:
            error = "Runner ID is required"
        else:
            db.execute("SELECT runner_id FROM year{} WHERE game_id = %s".format(year_level), (chaser_id))
            if db.fetchone() != runner_id:
                valid = False
                error = "Please double check your year level, Chaser ID and Runner ID."
            db.execute("INSERT INTO caught (chaser_id, runner_id, valid) values (%s, %s, %s)", (chaser_id, runner_id, valid))
        if error is None:
            db.execute("")
    return render_template("forms/caught.html")

@bp.route("/op_out", methods=["GET", "POST"])
def op_out():
    return render_template("forms/op_out.html")

@bp.route("/reassign", methods=["GET", "POST"])
def reassign():
    return render_template("forms/reassign.html")

@bp.route("/report", methods=["GET", "POST"])
def report():
    return render_template("forms/report.html")
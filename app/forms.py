from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request
)

from .db import get_db
from .emailing import email_caught, email_reassign

bp = Blueprint("forms", __name__, url_prefix="/forms")

@bp.route("/")
def forms():

    """Render the main page, containing links to other forms."""

    return render_template("forms/all_forms.html")

@bp.route("/caught", methods=["GET", "POST"])
def caught():

    """
    Render caught form, take chaser_id and runner_id, 
    then eliminate the runner, is the redentials match.
    """

    if request.method == "POST":
        # Get frontend form values.
        chaser_id = request.form["chaser_id"]
        runner_id = request.form['runner_id']
        valid = False
        # Get database connection.
        cnx, cursor = get_db()
        message = None
        # Exceptions. Both field must be filled.
        if not chaser_id:
            message = "Chaser ID is required."
        elif not runner_id:
            message = "Runner ID is required."
        else:
            # Get the actual runner based on the inputted chaser_id.
            cursor.execute(f"SELECT runner_id FROM all_players WHERE chaser_id = '{chaser_id}'")
            try:
                # Check ids. 
                if cursor.fetchone()['runner_id'] != runner_id:
                    message = "Please double check your Chaser ID and Runner ID."
            # if cursor return none type then chaser id is invalid
            except TypeError:
                # When no results are returned based on that chaser_id.
                message = "Invalid Chaser ID."
        if message is None:
            # Set runner's game status to dead.
            cursor.execute(f"UPDATE all_players SET game_status = 'dead' WHERE chaser_id = '{runner_id}'")
            # Update chaser's score (caught_count).
            cursor.execute(f"UPDATE all_players SET caught_count = caught_count + 1 WHERE chaser_id = '{chaser_id}'")
            try:
                email_caught(runner_id, chaser_id)
                message = "Congratulations!"
            except:
                message = "Sorry, something is wrong. Please Contact the Chase team."
            valid = True
        cursor.execute("INSERT INTO caught (chaser_id, runner_id, valid) values (%s, %s, %s)", (chaser_id, runner_id, valid))
        cnx.commit()
        flash(message)
    return render_template("forms/caught.html")

@bp.route("/opt_out", methods=["GET", "POST"])
def opt_out():
    if request.method == "POST":
        # Get frontend form values.
        email = request.form['email']
        reasons = request.form['reasons']
        valid = False
        # Get database connection.
        cnx, cursor = get_db()
        message = None
        # Email field must be filled. 
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
            # Update the database.
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
        # Get frontend form values
        chaser_id = request.form["chaser_id"]
        fname = request.form['fname']
        valid = False
        # Get database connection
        cnx, cursor = get_db()
        message = None
        # All fields must be filled.
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
            # Update original runner's status.
            cursor.execute(f"UPDATE all_players SET game_status = 'absent', chaser_count = chaser_count - 1 WHERE chaser_id = '{chaser['runner_id']}'")
            # Select new runner who is in the same year level, different house.
            cursor.execute(f"SELECT fname, lname, chaser_id FROM all_players WHERE house <> '{chaser['house']}' AND year_level = {chaser['year_level']} AND game_status = 'alive' ORDER BY chaser_count LIMIT 1")
            new_runner = cursor.fetchone()
            # Update chaser's information.
            cursor.execute(f"UPDATE all_players SET runner_id = '{new_runner['chaser_id']}', reassign_count = reassign_count + 1 WHERE chaser_id = '{chaser_id}'")
            # Update new runner's information.
            cursor.execute(f"UPDATE all_players SET chaser_count = chaser_count + 1 WHERE chaser_id = '{new_runner['chaser_id']}'")
            message = f"Successful. You new runner is {new_runner['fname']} {new_runner['lname']}"
            valid = True
        cursor.execute("INSERT INTO reassign (chaser_id, fname, valid) values (%s, %s, %s)", (chaser_id, fname, valid))
        cnx.commit()
        flash(message)
        email_reassign(chaser_id, new_runner['chaser_id'])
    return render_template("forms/reassign.html")

@bp.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        # Get frontend form values.
        email = request.form['email']
        report = request.form['report']
        # Get database connection.
        cnx, cursor = get_db()
        message = None
        # Email must be filled. 
        if not email:
            message = "Your email adress is required."
        else:
            cursor.execute(f"SELECT game_status FROM all_players WHERE email = '{email}'")
            player = cursor.fetchone()
            if not player:
                message = "Invalid email."
        cursor.execute("INSERT INTO report (email, message) values (%s, %s)", (email, report))
        message = "Thank you. We will get back to you."
        cnx.commit()
        flash(message)
    return render_template("forms/report.html")
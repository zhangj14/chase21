import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

import click
from flask.cli import with_appcontext

from .db import get_db
from . import config

def email_runner():
    # Creating variables
    print("Creating variables...")
    now = datetime.now()
    date = now.strftime("%d")
    month = now.strftime("%m")
    day = now.strftime("%A")

    # get database connection and cursor
    cnx, cursor = get_db()
    # select email adress and information needed for email
    cursor.execute("select a.id, a.chaser_id, a.email, \
        b.fname as Rfname, b.lname as Rlname, b.form as Rform \
        from all_players a, all_players b \
        where a.id <> b.id and a.runner_id = b.chaser_id \
        and a.game_status = 'alive'")
    all = cursor.fetchall()

    html_email = """
    <h1>Newlands College Chase 2021</h1>
    <p style="font-size: 1.5em;">Your Player ID is <span style="color: #ffffff; background-color: #3e3874;"><strong>{player_id}</strong></span></p>
    <p style="font-size: 1.5em;">Your Runner is <span style="color: #ffffff; background-color: #3e3874;"><strong>{runner_first_name} {runner_last_name}</strong></span>&nbsp;from&nbsp;<span style="color: #ffffff;background-color: #3e3874;"><strong>{runner_form}</strong></span></p>
    <p>To catch your runner, place a peg on them, then obtain their player ID. Fill out the <a href="https://forms.gle/vorfm6X2JbiGdSbw8" target="_blank" rel="noopener">caught form</a> to report the catch!</p>
    <p><a href="https://sites.google.com/newlands.school.nz/nc-chase/home" target="_blank" rel="noopener">Detailed rules and more information at our website.</a></p>
    <h4><p>Runner not at school? Fill out our <a href="https://forms.gle/2KZcZPGYvRMftsDr6" target="_blank" rel="noopener">reassign form</a> to get a new runner.</p></h4>
    <p>Remember to keep your Player ID secret!</p>
    <p>Pegs must be clipped onto the body or clothing, not bags.</p>
    <br>
    <p style="font-size:1.2em;">This email was sent automatically - for assistance, reply to this email or message us on Instagram 
    <a href="https://www.instagram.com/newlands.college.chase/" target="_blank" rel="noopener">@newlands.college.chase</a></p>
    <h3>Telling a friend could be telling the enemy, so keep your lips sealed! Good luck.</h3>
    <h2><a href="https://bit.ly/NCChase" target="_blank" rel="noopener">Chase21 Website</a></h2>
    """


    message = MIMEMultipart("alternative")
    message["Subject"] = "NC Chase21 -  " + day + " " + date + "/" + month
    message["From"] = "Gamemaster <gamemaster@newlands.school.nz>"
    message["To"] = "Players <NC-Chase21>"

    print("Emails sending now...")

    # Create Context for server
    context = ssl.create_default_context() 

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Greet the server
        server.ehlo_or_helo_if_needed()
        server.login(config.email_address, config.email_password)
        counter = 0
        for person in all:
            counter += 1
            # for testing purposes
            # if person['email'] == "zhangj@newlands.school.nz" or person['email'] == 'taefuj@newlands.school.nz' or person['email'] == 'khallafm@newlands.school.nz' or person['email'] == 'kahja@newlands.school.nz':
                # pause every 30 mails due to quota restriction
            if counter % 30 == 0:
                time.sleep(31)

            part_html = MIMEText(html_email.format(runner_form=person['Rform'], runner_first_name=person['Rfname'], runner_last_name=person['Rlname'], player_id=person['chaser_id']), "html")

            message.attach(part_html)
            server.sendmail(config.email_address, person['email'], message.as_string())
        print(counter, "mail(s) sent.")


def email_caught(runner_id, chaser_id):

    # get database connection and cursor
    cnx, cursor = get_db()
    # select email adress and information needed for email
    cursor.execute(f"select email, chaser_id, fname, lname, \
                   from all_players where runner_id = '{runner_id}'")
    chasers = cursor.fetchall()
    cursor.execute(f"select email, fname, lname, \
                    from all_players where chaser_id = '{chaser_id}'")
    runner = cursor.fetchone()
    # Creating variables for tiem and date (these go in the subject of the email)
    print("Creating variables...")
    now = datetime.now()
    # current date and time
    date = now.strftime("%d")
    month = now.strftime("%m")
    day = now.strftime("%A")
        
    html_email = """
                <h1><strong>Newlands College Chase 2021 <span style="color: #ff0000;">Caught Notice</span></strong></h1>
                <h4>Sadly, for you, the game is over... You have been caught by your Chaser...</h4>
                <p>You will no longer receive a runner, or have someone chasing you. However, you can still help your house, or participate in other Chase21 Events!</p>
                <p>If you disagree or have any questions, you can reach out by replying or messaging us on Instagram <a href="https://www.instagram.com/newlands.college.chase/" target="_blank" rel="noopener">@newlands.college.chase</a></p>
                <i>Your battle was a fierce one, one of deception, one of wit, one that sadly, <strong>you lost.</strong></i>
                <p style="font-size: 1.2em;">This email was sent automatically - for assistance, reply to this email or message us on Instagram <a href="https://www.instagram.com/newlands.college.chase/" target="_blank" rel="noopener">@newlands.college.chase</a></p>
                <h2><a href="https://bit.ly/NCChase" target="_blank" rel="noopener">Chase21 Website</a></h2>
                """

    
    # for student in sheet_data:
    message = MIMEMultipart("alternative")
    message["Subject"] = "NC Chase21 Exec -  " + day + " " + date + "/" + month
    message["From"] = "Gamemaster <gamemaster@newlands.school.nz>"
    message["To"] = "Players <NC-Chase21>"
    # message["Reply-To"] = ""

    print("Emails sending now...")

    context = ssl.create_default_context() # Create Context for server

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

        server.ehlo_or_helo_if_needed() # Greet the server
        # server.starttls() # Establish Secure Connection with server

        # print(email_address, email_password, "email details")
        server.login(config.email_address, config.email_password)
        
        # Retrieving email of recipient & that persons ID.
        receiver_email = runner["email"]

        # Creating, attaching and sending the email
        part_html = MIMEText(html_email.format(player_id=chaser_id), "html")
        message.attach(part_html)
        server.sendmail(config.email_address, receiver_email, message.as_string())


    # print(str(person + 1) + " emails sent")

    # Send logging message that an email has been sent.
    Logging.complete("EmailRunners.py", year, str(counter) + " email(s) sent")

# register commands to the app
@click.command("email-runner")
@with_appcontext
def email_runner_command():
    if (input("WARNING!!!\
        \nSending emails to ALL alive players.\
        \nDo you want to proceed? (y/n) ") == "y"):
        email_runner()
        click.echo("Emailed runner.")
    else:
        click.echo("Cancelled.")

# @click.command("assign-id")
# @with_appcontext
# def assign_id_command():
#     Admin().assign_ID()
#     click.echo("Assigned chaser IDs.")

def init_app(app):
    app.cli.add_command(email_runner_command)
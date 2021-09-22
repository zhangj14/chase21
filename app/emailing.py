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

    """
    Send emails to all alive players at the beginning of a game day.
    """

    # Obtaining dates for the email. 
    print("Getting the date...")
    now = datetime.now()
    date = now.strftime("%d")
    month = now.strftime("%m")
    day = now.strftime("%A")

    # Get database connection and cursor.
    cnx, cursor = get_db()
    # Select email adress and information needed for email.
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

    # Formatting the subject of the email.
    message = MIMEMultipart("alternative")
    message["Subject"] = "NC Chase21 -  " + day + " " + date + "/" + month
    message["From"] = "Gamemaster <gamemaster@newlands.school.nz>"
    message["To"] = "Players <NC-Chase21>"

    print("Emails sending now...")

    # Create Context for server.
    context = ssl.create_default_context() 

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Greet the server.
        server.ehlo_or_helo_if_needed()
        # Login with the credentials provided.
        server.login(config.email_address, config.email_password)
        counter = 0
        for person in all:
            if person['email'] != "zhangj@newlands.school.nz" and person['email'] != "john.china.3204@gmail.com":
                continue
            if counter >= 2:
                break
            else:
                counter += 1
                if counter % 30 == 0:
                    time.sleep(31)

                part_html = MIMEText(html_email.format(runner_form=person['Rform'], runner_first_name=person['Rfname'], runner_last_name=person['Rlname'], player_id=person['chaser_id']), "html")

                message.attach(part_html)
                server.sendmail(config.email_address, person['email'], message.as_string())
        print(counter, "mail(s) sent.")


def email_caught(runner_id, chaser_id):

    """
    Send email to the runner who's caught, 
    and send emails to the chasers
    """

    # Get database connection and cursor.
    cnx, cursor = get_db()
    # Select email adress and information needed for email.
    cursor.execute(f"select email, chaser_id, fname, lname \
                   from all_players where runner_id = '{runner_id}'")
    chasers = cursor.fetchall()
    cursor.execute(f"select email, fname, lname \
                    from all_players where chaser_id = '{runner_id}'")
    runner = cursor.fetchone()
    # Getting time and date (these go in the subject of the email).
    print("Creating variables...")
    now = datetime.now()
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

    
    # Formatting the subject of the email. 
    message = MIMEMultipart("alternative")
    message["Subject"] = "NC Chase21 Exec -  " + day + " " + date + "/" + month
    message["From"] = "Gamemaster <gamemaster@newlands.school.nz>"
    message["To"] = "Players <NC-Chase21>"

    print("Emails sending now...")

    # Create context for the server
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

        # Greet the server
        server.ehlo_or_helo_if_needed()
        # Login using credentials provided in config.py.
        server.login(config.email_address, config.email_password)
        
        # Creating, attaching and sending the email.
        part_html = MIMEText(html_email.format(player_id=chaser_id), "html")
        message.attach(part_html)
        server.sendmail(config.email_address, runner['email'], message.as_string())

        for chaser in chasers:
            if chaser['chaser_id'] == chaser_id:
                server.sendmail(config.email_address, chaser['email'], f"Congrats {chaser['fname']} {chaser['lname']}")
            else:
                server.sendmail(config.email_address, chaser['email'], f"Sorry {chaser['fname']} {chaser['lname']}")

def email_reassign(chaser_id, runner_id):

    """
    Send email to to the people who requested valid reassign.
    """
    
    # Get database connection and cursor.
    cnx, cursor = get_db()
    # Select email adress and information needed for email.
    cursor.execute(f"select email \
                   from all_players where chaser_id = '{chaser_id}'")
    chaser = cursor.fetchone()
    cursor.execute(f"select fname, lname, form \
                    from all_players where chaser_id = '{runner_id}'")
    runner = cursor.fetchone()
    # Creating variables for tiem and date (these go in the subject of the email).
    print("Creating variables...")
    now = datetime.now()
    # Current date and time.
    date = now.strftime("%d")
    month = now.strftime("%m")
    day = now.strftime("%A")
        
    html_email = """
        <h1>Newlands College Chase 2021</h1>
        <p style="font-size: 1.5em;">Your <strong>NEW<strong> Runner is <span style="color: #ffffff; background-color: #3e3874;"><strong>{runner_first_name} {runner_last_name}</strong></span>&nbsp;from&nbsp;<span style="color: #ffffff;background-color: #3e3874;"><strong>{runner_form}</strong></span></p>
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

    
    # For student in sheet_data:
    message = MIMEMultipart("alternative")
    message["Subject"] = "NC Chase21 Exec -  " + day + " " + date + "/" + month
    message["From"] = "Gamemaster <gamemaster@newlands.school.nz>"
    message["To"] = "Players <NC-Chase21>"

    print("Emails sending now...")

    # Create context for the server.
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Greet the server.
        server.ehlo_or_helo_if_needed()
        server.login(config.email_address, config.email_password)

        # Creating, attaching and sending the email
        part_html = MIMEText(html_email.format(runner_first_name=runner['fname'], runner_last_name=runner['lname'], runner_form=runner['form']), "html")
        message.attach(part_html)
        server.sendmail(config.email_address, chaser['email'], message.as_string())

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

def init_app(app):
    app.cli.add_command(email_runner_command)
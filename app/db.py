import click
from flask import g
from flask.cli import with_appcontext
import mysql.connector
from . import config

def get_db(dict=True):
    """
    To return database connection and a cursor. 
    The returned values of cursor queries are default to dictionaries.
    """
    # Get database connection.
    # If connection exists in g, return db stored in g.
    # If not, create new connection, add to g, then return.
    if "db" not in g:
        db = mysql.connector.connect(**config.mysql)
        cursor = db.cursor(dictionary=dict)
        return db, cursor

def close_db(e=None):
    """
    Remove database from current session, close cursor and connection.
    """
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    """
    Initialize the database with a csv file provided by the school 
    including first name, lastname, formclass, house and email.
    """
    # Get db connection.
    db, cursor = get_db()
    # With clause is used for error handling and closing the file properly.
    with open("app/schema.sql") as f:
        # Mulit used to return an iterator.
        result_iterator = cursor.execute(f.read(), multi=True)
        for r in result_iterator:
            # Will print out a short representation of the query.
            print("Running query: ", r)  
            print(f"Affected {r.rowcount} rows" )

# Add command to the app.
@click.command("init-db")
@with_appcontext
def init_db_command():
    decision = input("WARNING! This command initializes the whole database, \
current game information will be lost. \
\n(y/n)?")
    if decision == 'y' or decision == 'Y':
        init_db()
        click.echo("Initialized the database.")
    else:
        print("Aborted")

# Register with the application
def init_app(app):
    # Close db to clean up after returning a response.
    app.teardown_appcontext(close_db)
    # Add command to the app.
    app.cli.add_command(init_db_command)
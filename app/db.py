import click
from flask import g
from flask.cli import with_appcontext
import mysql.connector
from . import config
def get_db(dict=True):
    # get database connection
    # if connection exists in g, return db stored in g
    # if not, create new connection, add to g, then return
    # if "db" not in g:
    db = mysql.connector.connect(**config.mysql)
    cursor = db.cursor(dictionary=dict)
    return db, cursor

def close_db(e=None):
    # remove database from current session
    # close cursor and connection
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    # get db connection
    db, cursor = get_db()
    # with clause is used for error handling and close the file properly
    with open("app/schema.sql") as f:
        # mulit used to return an iterator
        result_iterator = cursor.execute(f.read(), multi=True)
        for r in result_iterator:
            # Will print out a short representation of the query
            print("Running query: ", r)  
            print(f"Affected {r.rowcount} rows" )

# add command to cmd
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

# register with the application
def init_app(app):
    # close db to clean up after returning a response
    app.teardown_appcontext(close_db)
    # add command to the app
    app.cli.add_command(init_db_command)
import mysql.connector
import click
from flask.cli import with_appcontext

from random import shuffle
from operator import itemgetter
from datetime import datetime

from .db import get_db

def assign_ID():

    """to assign random IDs to all players run at the beginning of
    the day, select only alive people.
    """

    # Establish db connection, create cursor.
    cnx, cursor = get_db()

    # Create and randomize chaser_ids.
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "R", "T", "X"]
    id_list = []
    for letter in letters:
        new_letter_list = [letter + "{}".format(i) for i in range(101, 500)]
        id_list += new_letter_list
    shuffle(id_list)

    # Select alive people's ids.
    cursor.execute("SELECT id FROM all_players WHERE game_status = 'alive'")
    alive_id = cursor.fetchall()

    row_count = 0
    for i in range(len(alive_id)):
        # Update their chaser ids, remove used ids.
        cursor.execute(f"UPDATE all_players \
                            SET chaser_id = '{id_list.pop()}', \
                                chaser_count = 0 \
                            WHERE id = {alive_id[i]['id']}")
        row_count += 1

    print("{} row(s) affected.".format(row_count))
    cnx.commit()

def assign_runner():

    'to assign random runners within each year group'

    # Establish db connection, create cursor.
    cnx, cursor = get_db()
    # Handle different year levels seperately.
    for year_level in range(9, 13):

        # Fetch all alive players within a year group as a pool.
        print("\nSelecting alive players year{}.".format(year_level))
        cursor.execute(f"SELECT chaser_id, chaser_count, house \
                        FROM all_players WHERE game_status = 'alive' \
                        AND year_level = {year_level}")
        all_alive = cursor.fetchall()
        print("{} row(s) selected.".format(len(all_alive)))

        # Randomize first, then sort by number of chasers.
        shuffle(all_alive)
        all_alive.sort(key = itemgetter('chaser_count'))

        # Fetch house names, sort by number of players alive.
        cursor.execute(f"SELECT house as name, COUNT(house) as count FROM all_players \
                        WHERE game_status = 'alive' AND year_level = {year_level} \
                        GROUP BY house \
                        ORDER BY COUNT(house) DESC")
        houses = cursor.fetchall()
        for house in houses:
            print(f"{house['name']} : {house['count']} people alive.")

        # Pointer for runner.
        j = 0
        row_count = 0
        for house in houses:

            # Select alive people in a house.
            print("Assigning alive year{} in {}...".format(year_level, house))
            cursor.execute(f"SELECT id FROM all_players \
                            WHERE game_status = 'alive' \
                            AND house = '{house['name']}' \
                            AND year_level = {year_level} ")
            house_alive = cursor.fetchall()

            for current in house_alive:
                # Find person who's not in the chaser's house.
                try:
                    while all_alive[j]['house'] == house:
                        j += 1
                except IndexError:
                    # Reset runner pool.
                    shuffle(all_alive)
                    all_alive.sort(key = itemgetter('chaser_count'))
                    j = 0
                # Update database.
                cursor.execute(f"UPDATE all_players \
                                    SET runner_id = '{all_alive[j]['chaser_id']}' \
                                    WHERE id = {current['id']}")
                cursor.execute(f"UPDATE all_players \
                                    SET chaser_count = chaser_count + 1 \
                                    WHERE chaser_id = '{all_alive[j]['chaser_id']}'")
                row_count += 1
                # Increase the chaser count of the runner.
                all_alive[j]['chaser_count'] += 1
                # Move the pointer.
                j += 1
    cnx.commit()

# register commands to the app
@click.command("assign-runner")
@with_appcontext
def assign_runner_command():
    assign_runner()
    click.echo("Assigned runner.")

@click.command("assign-id")
@with_appcontext
def assign_id_command():
    assign_ID()
    click.echo("Assigned chaser IDs.")

def init_app(app):
    app.cli.add_command(assign_runner_command)
    app.cli.add_command(assign_id_command)
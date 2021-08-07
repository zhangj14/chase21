from flask import cli
import mysql.connector
import click
from flask.cli import with_appcontext

from random import shuffle
from operator import itemgetter
from datetime import datetime

from .config import mysql as db_config

class Admin:
    """Admin object including functions such as assign chaser IDs, assign runners"""

    # Establish connection.
    cnx = mysql.connector.connect(**db_config)
    cnx.database = "nc_chase_3"

    # Obtain cursor to execute queries.
    cursor = cnx.cursor()
    
    def assign_ID(self):

        """to assign random IDs to all players run at the beginning of
        the day, select only alive people.
        """

        # Create ids.
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "R", "T", "X"]
        id_list = []
        for letter in letters:
            new_letter_list = [letter + "{}".format(i) for i in range(101, 500)]
            id_list += new_letter_list
        shuffle(id_list)

        # select alive people's ids
        self.cursor.execute("SELECT id FROM all_players WHERE game_status = 'alive'")
        alive_id = self.cursor.fetchall()

        row_count = 0
        for i in range(len(alive_id)):
            # Update their chaser ids, remove used ids.
            self.cursor.execute(f"UPDATE all_players \
                                SET chaser_id = '{id_list.pop()}', \
                                    chaser_count = 0 \
                                WHERE id = {alive_id[i][0]}")
            row_count += 1

        print("{} row(s) affected.".format(row_count))
        self.cnx.commit()

    def assign_runner(self):

        'to assign random runners within each year group'
        # Handle different year levels seperately.
        for year_level in range(9, 13):

            # Fetch all alive players within a year group as a pool.
            print("\nSelecting alive players year{}.".format(year_level))
            self.cursor.execute(f"SELECT chaser_id, chaser_count, house \
                                FROM all_players WHERE game_status = 'alive' \
                                AND year_level = {year_level}")
            all_alive = [list(i) for i in self.cursor.fetchall()]
            print("{} row(s) selected.".format(len(all_alive)))
            # Randomize first, then sort by number of chasers.
            shuffle(all_alive)
            all_alive.sort(key = itemgetter(1))

            # Fetch house names, sort by number of players alive.
            self.cursor.execute(f"SELECT house, COUNT(house) FROM all_players \
                                WHERE game_status = 'alive' AND year_level = {year_level} \
                                GROUP BY house \
                                ORDER BY COUNT(house) DESC")
            houses = {name[0]: name[1] for name in self.cursor.fetchall()}
            for house in houses.keys():
                print("{} : {} people alive.".format(house, houses[house]))

            # Pointer for runner.
            j = 0
            row_count = 0
            for house in houses:

                # Select alive people in a house.
                print("Assigning alive year{} in {}...".format(year_level, house))
                self.cursor.execute(f"SELECT id FROM all_players \
                                    WHERE game_status = 'alive' \
                                    AND house = '{house}' \
                                    AND year_level = {year_level} ")
                house_alive = self.cursor.fetchall()

                for current in house_alive:
                    # Find person who's not in the chaser's house.
                    try:
                        while all_alive[j][2] == house:
                            j += 1
                    except IndexError:
                        # Reset runner pool.
                        shuffle(all_alive)
                        all_alive.sort(key = itemgetter(1))
                        j = 0
                    # Update database.
                    self.cursor.execute(f"UPDATE all_players \
                                        SET runner_id = '{all_alive[j][0]}' \
                                        WHERE id = {current[0]}")
                    self.cursor.execute(f"UPDATE all_players \
                                        SET chaser_count = chaser_count + 1 \
                                        WHERE chaser_id = '{all_alive[j][0]}'")
                    row_count += 1
                    # Increase the chaser count of the runner.
                    all_alive[j][1] += 1
                    # Move the pointer.
                    j += 1
        self.cnx.commit()

# register commands to the app
@click.command("assign-runner")
@with_appcontext
def assign_runner_command():
    Admin().assign_runner()
    click.echo("Assigned runner.")

@click.command("assign-id")
@with_appcontext
def assign_id_command():
    Admin().assign_ID()
    click.echo("Assigned chaser IDs.")

def init_app(app):
    app.cli.add_command(assign_runner_command)
    app.cli.add_command(assign_id_command)
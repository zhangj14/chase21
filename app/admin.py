from flask import cli
import mysql.connector
import click
from flask.cli import with_appcontext

from random import shuffle
from operator import itemgetter
from datetime import datetime

from .config import mysql as db_config

class LinkedList:
    """Linked list class for fast insertion and poping. Used for assign runners"""
    class Node:
        def __init__(self, prev = None, person = None, next = None) -> None:
            self.prev = prev
            self.person = person
            self.next = next

    first = Node()
    
    def is_empty(self) -> bool:
        return self.first == None

    def push(self, person) -> None:
        if person == None:
            raise TypeError
        old_first = self.first
        self.first.person = person
        self.first.next = old_first
        self.first.pre

class Person:
    """Person class to include individual player's information. 
       Instead of treating them as nested lists"""
    def __init__(self, **kwargs) -> None:
        self.id = kwargs['id']
        self.chaser_count = kwargs['chaser_count']
        self.house = kwargs['house']

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
    
    def reassign(self) -> None:
        def get_all_requests() -> list:
            """return all requests sent today"""
            unhandled = self.cursor.execute("SELECT * FROM reassign \
                                            WHERE DATE(timestamp) = CURDATE()")
            return unhandled

        def update_away_people(requests) -> None:
            """Mark all people who are reported away of a year level."""
            for request in requests:
                self.cursor.execute(f"UPDATE all_players, \
                                    (SELECT runner_id, chaser_id \
                                    FROM all_players) AS ref \
                                    SET all_players.game_status = 2 \
                                    WHERE all_players.chaser_id = ref.runner_id \
                                    AND ref.chaser_id = '{request[3]}' \
                                    LIMIT 1")
            self.cnx.commit()


        def reassign():
            requests = get_all_requests()
            # Handle different year levels.
            for year_level in range(9, 13):
                # if no request from a year level, skip
                if not(requests['year{}'.format(year_level)]):
                    continue
                update_away_people(requests['year{}'.format(year_level)], year_level)
                # select alive people in a year level.
                self.cursor.execute(f"SELECT game_id, chaser_count, house \
                                    FROM year{year_level} WHERE game_status = 0")
                all_alive = [list(i) for i in self.cursor.fetchall()]
                # Randomize then sort by number of chasers 
                # to make game as fair as possible
                shuffle(all_alive)
                all_alive.sort(key = itemgetter(1))
                j = 0

                for current in requests['year{}'.format(year_level)]:
                    # find person who's not in the chaser's house
                    try:
                        while all_alive[j][2] == current[5]:
                            j += 1
                    except IndexError:
                        # reset runner pool
                        shuffle(all_alive)
                        all_alive.sort(key = itemgetter(1))
                        j = 0

                    # update database
                    self.cursor.execute(f"UPDATE year{year_level} \
                                        SET runner_id = '{all_alive[j][0]}' \
                                        WHERE game_id = {current[3]}")
                    self.cursor.execute(f"UPDATE year{year_level} \
                                        SET chaser_count = chaser_count + 1 \
                                        WHERE game_id = '{all_alive[j][0]}'")
                    # increase the chaser count of the runner
                    all_alive[j][1] += 1
                    # move the pointer
                    j += 1
            self.cursor.execute()
            self.cnx.commit()
        reassign()

                
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

@click.command("reassign")
@with_appcontext
def reassign_command():
    Admin().assign_ID()
    click.echo("Reassigned runner IDs.")
def init_app(app):
    app.cli.add_command(assign_runner_command)
    app.cli.add_command(assign_id_command)
    app.cli.add_command(reassign_command)
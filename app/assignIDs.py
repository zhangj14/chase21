from random import shuffle
from . import connectDB

def assignIDs():
    list_of_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "M", "R", "T", "X"]
    all_id_list = []
    for letter in list_of_letters:
        new_letter_list = [[letter + "{}".format(i)] for i in range(101, 500)]
        all_id_list += new_letter_list
    shuffle(all_id_list)
    cnx = connectDB.connection()
    cursor = cnx.cursor()

    cursor.executemany("")
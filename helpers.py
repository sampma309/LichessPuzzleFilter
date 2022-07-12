import sqlite3
from sqlite3 import Error
import chess
import base64
import json

def create_connection(path):
    """Creates and returns a connection to the local copy of the Lichess puzzle
       database.

        Arguments:

         - path: location of the database. This should always be puzzles.db since
                 the database and app.py are in the same level of the directory
        
        Returns:

         - a Connection object that represents the database
    """

    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def find_puzzle(pieces, lower_rating, upper_rating):
    """Finds and returns puzzles that contain only pieces specified by the user

        Arguments:

         - pieces: a string containing both the upper and lower case letters
                      of the user-specified pieces (e.g., pPrR) would be for
                      pawns and rooks
        
        Returns:

         - puzzle:    A two column list of the puzzles returned by the SQL query.
                      The first column contains the FEN for the starting position
                      of the puzzle. The second column contains a list of the 
                      correct moves in UCI notation.
    """

    # Connect to database and execute query
    db = create_connection('puzzles.db')
    cursor = db.cursor()
    puzzles = {'PuzzleId': [], 'Moves': [], 'Rating': [], 'EncodedURL': []}
    for row in cursor.execute("SELECT Moves, Rating, PuzzleId, EncodedURL FROM puzzles WHERE Pieces = (?) AND RATING >= ? AND RATING <= ? ORDER BY RANDOM()", [pieces, lower_rating, upper_rating]):
        puzzles['PuzzleId'].append(row[2])
        puzzles['Moves'].append(row[0])
        puzzles['Rating'].append(row[1])
        puzzles['EncodedURL'].append(row[3])

    # Write dictionary to JSON file
    with open('static/puzzles.json', 'w') as file:
        json.dump(puzzles, file)
    return None

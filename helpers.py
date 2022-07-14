import sqlite3
from sqlite3 import Error
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
    db = create_connection('static/puzzles.db')
    cursor = db.cursor()

    # Get random puzzle from DB
    puzzle = []
    for row in cursor.execute("SELECT Moves, Rating, PuzzleId, EncodedURL FROM puzzles WHERE Pieces = (?) AND RATING >= ? AND RATING <= ? ORDER BY RANDOM() LIMIT 1", [pieces, lower_rating, upper_rating]):
        # Append moves
        puzzle.append(row[0])
        #Append Rating
        puzzle.append(row[1])
        # Append ID
        puzzle.append(row[2])
        # Append URL
        puzzle.append(row[3])
    
    return puzzle

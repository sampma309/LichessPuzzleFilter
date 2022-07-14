import sqlite3
import base64
from sqlite3 import Error

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

         - pieces:  a string containing both the upper and lower case letters
                    of the user-specified pieces (e.g., pPrR) would be for
                    pawns and rooks

         - lower/upper_rating:  the lower and upper bounds for the puzzle difficulty
        
        Returns:

         - puzzle:  a four-element list containing the solution move list in SAN notation,
                    the puzzle rating, the puzzle ID on Lichess, and the encoded URL needed
                    to generate the embedded puzzle.  
    """

    # Connect to database and execute query
    db = create_connection('static/puzzles.db')
    cursor = db.cursor()

    # Get random puzzle from DB
    puzzle = []
    for row in cursor.execute("SELECT Moves, Rating, PuzzleId, LastMove, FEN FROM puzzles WHERE Pieces = (?) AND RATING >= ? AND RATING <= ? ORDER BY RANDOM() LIMIT 1", [pieces, lower_rating, upper_rating]):
        
        # Collect the puzzle information
        puzzle.append(row[0])  # Append moves
        puzzle.append(row[1])  # Append Rating
        puzzle.append(row[2])  # Append ID
        puzzle.append(row[3])  # Append last move
        puzzle.append(row[4])  # Append FEN
    
    return puzzle

def encode_puzzle(puzzle):
    """In acccordance with the Listudy documentation (https://listudy.org/en/webmaster/custom-tactics),
       this function gathers the FEN of the starting position, the correct variation, and 
       the previous move and creates a string that will be used as the src in an embedded
       iframe containing the puzzle."""

    # Get necessary information from the puzzle
    fen = puzzle[4]
    moves = puzzle[0].split()
    last_move = puzzle[3]

    # Create the string to encode
    encode_string = f"{fen};{moves};{last_move}"
            
    # Encode the string
    return base64.standard_b64encode(encode_string.encode()).decode('utf-8')


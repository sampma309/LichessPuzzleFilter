import sqlite3
from sqlite3 import Error
import chess
import base64

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
    puzzles = []
    for row in cursor.execute("SELECT FEN, Moves, LastMove, Rating, PuzzleId FROM puzzles WHERE Pieces = (?) AND RATING >= ? AND RATING <= ? ORDER BY RANDOM()", [pieces, lower_rating, upper_rating]):
        puzzles.append(row)
        
    
    # Return list of puzzles
    print(puzzles)
    return puzzles


def encode_puzzle(puzzle):
    """Accepts a single puzzle as a list with two elements and returns the 64-bit encoded
       hash that can be used to embed the puzzle according to Listudy documentation.
       (https://listudy.org/en/webmaster/custom-tactics)

        Arguments:

         - puzzle: a list with two elements, the first being a valid FEN and the second
                   being a space-separated list of correct moves to solve the tactic

        Returns:

         - a string that can be appended to the Listudy URL to embed a custom tactic into
           a webpage
    """
    
    # Parse input
    fen = puzzle[0]
    moves = puzzle[1].split()
    board = chess.Board(fen)

    # Create the three pieces of the hashed string per Listudy documentation
    variation = []
    last_move = puzzle[2]
    while moves:
        move = moves.pop(0)
        variation.append(board.san(chess.Move.from_uci(move)))
        move_on_board = chess.Move.from_uci(move)
        board.push(move_on_board)
    variation = ' '.join(variation)

    # Create the string to encode
    encode_string = f"{fen};{variation};{last_move}"
    
    # Encode the string
    listudy_encode = base64.standard_b64encode(encode_string.encode())

    # Return the encoded byte string as a string
    return listudy_encode.decode('utf-8')
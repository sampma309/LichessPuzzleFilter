"""This program creates a SQLite database from a CSV file which can be downloaded
   from Lichess. In order to parse the puzzles correctly, the CSV file must be named
   'puzzles.csv' and no additional columns may be added or removed from the as-downloaded 
   file, although lines can be deleted if you wish to work with only a subset of the 
   full 2.6 million puzzle database."""


import helpers
import chess
from sqlite3 import Error
import csv
import base64


def main():

    # Create connection to puzzles.db
    db = helpers.create_connection('puzzles.db')

    # Create table 'puzzles' in puzzles.db
    create_table(db)
    
    # Read data from puzzles.csv and import to puzzles.db
    import_data('puzzles.csv', db)

    # Create index on PuzzleId column to speed up remaining steps
    db.execute('CREATE INDEX PuzzleIdIndex ON puzzles (PuzzleId);')

    # Make the first move in each puzzle and update the FEN and move list
    update_fen(db)

    # Create a new column containing each players pieces
    create_piece_list(db)

    # Create index on Pieces column so webpage will return puzzles more quickly
    db.execute('CREATE INDEX PiecesIndex ON puzzles (Pieces);')

    # Create encoded URLs column
    encode_puzzles(db)

    db.commit()
    db.close()


def create_table(db):
    
    try:
        db.execute('CREATE TABLE puzzles("PuzzleId" TEXT, "FEN" TEXT, "Moves" TEXT, "LastMove" TEXT, "Rating" INTEGER, "Pieces" TEXT, "EncodedURL" TEXT);')
        print("Table 'puzzles' created successfully")
    except Error as e:
        print(f"The error '{e}' has occurred. Terminating program.")


def import_data(file, db):

    # Create database cursor for writing data
    cur = db.cursor()

    # Open file
    try:
        with open(file, newline='') as csvfile:

            # Create reader object
            reader = csv.reader(csvfile)

            # Print number of puzzles detected in the .csv file
            num_lines = len(list(reader))
            print(f"{num_lines} puzzles detected.")
            csvfile.seek(0)

            # Import puzzle data into puzzles.db
            for row in reader:
                cur.execute("INSERT INTO puzzles (PuzzleId, FEN, Moves, Rating) VALUES (?, ?, ?, ?);",
                           (row[0], row[1], row[2], int(row[3])))
                
                # Keep track of progress
                if reader.line_num % 10000 == 0:
                    print(f"{reader.line_num - num_lines} / {num_lines} puzzles imported")

    except IOError:
        print(f"Unable to open file '{file}'. Terminating program.")

    finally:
        csvfile.close()
    
def update_fen(db):

    cur = db.cursor()

    # Get all of the initial FENs and the moves for each puzzle
    original_lines = []
    counter = 0

    for row in cur.execute("SELECT PuzzleId, FEN, Moves FROM puzzles;"):
        original_lines.append([row[0], row[1], row[2]])
        
        counter += 1
        if counter % 5000 == 0:
            print(f"{counter} lines read")

    counter = 0

    # Iterate over every puzzle
    for line in original_lines:
        
        PuzzleId = line[0]
        original_fen = line[1]
        moves = line[2]
        
        # Make the first move in the puzzle, move it to the LastMove column 
        # and update the FEN
        moves = moves.split()
        board = chess.Board(original_fen)
        first_move = moves.pop(0)
        move_1 = chess.Move.from_uci(first_move)
        board.push(move_1)
        new_fen = board.fen()
        moves = ' '.join(moves)

        # Update the FEN and move list for the puzzle
        cur.execute("UPDATE puzzles SET FEN = ?, Moves = ?, LastMove = ? WHERE PuzzleId = ?;", [new_fen, moves, first_move, PuzzleId])
        
        counter += 1
        if counter % 10000 == 0:
            print(f"{counter} / {len(original_lines)} rows updated.")
    
    print("All FENs and move lists updated.")

def create_piece_list(db):
    cur = db.cursor()

    # Initialize list of FENs and pieces for each puzzle
    pieces = []
    fen_list = []
    counter = 0

    # Grab FENs from puzzle.db
    for row in cur.execute("SELECT FEN, PuzzleId FROM puzzles;"):
        fen_list.append([row[0], row[1]])

    # Iterate over each FEN
    for fen in fen_list:

        # Create new list of pieces and split the FEN into parts on each space
        pieces.append('')
        tmp = fen[0].split(' ')

        # If it is black to play, swap FEN case to maintain convention of upper-case
        # letters belonging to the player
        if tmp[1] == 'b':
            tmp[0] = tmp[0].swapcase()

        # Create a list of all pieces in the FEN, not including the king
        for char in tmp[0]:
            if char.isalpha() and char not in pieces[counter] and char not in ['k', 'K']:
                pieces[counter] += char

        # Sort the piece list so it can later be search for an exact match
        pieces[counter] = ''.join(sorted(pieces[counter]))

        # Add the pieces column 
        cur.execute("UPDATE puzzles SET Pieces = ? WHERE PuzzleId = ?;", [pieces[counter], fen[1]])
        counter += 1

        if counter % 10000 == 0:
            print(f"{counter} piece lists added")

    print("Piece lists complete.")

def encode_puzzles(db):
    cur = db.cursor()
    encoded_urls = []
    counter = 0

    # Get necessary information for each puzzle from DB
    for row in cur.execute("SELECT FEN, Moves, LastMove, PuzzleId FROM puzzles;"):
        fen = row[0]
        moves = row[1].split()
        last_move = row[2]
        board = chess.Board(fen)

        # Create the solution to the puzzle in algebraic notation
        variation = []
        while moves:
            move = moves.pop(0)
            variation.append(board.san(chess.Move.from_uci(move)))
            move_on_board = chess.Move.from_uci(move)
            board.push(move_on_board)
        variation = ' '.join(variation)

        # Create the string to encode
        encode_string = f"{fen};{variation};{last_move}"
                
        # Encode the string
        listudy_encode = base64.standard_b64encode(encode_string.encode()).decode('utf-8')
        encoded_urls.append([row[3], variation, listudy_encode])

        counter += 1

        if counter % 10000 == 0:
            print(f"{counter} puzzles encoded")

    for url in encoded_urls:

        # Add encoded URL column
        cur.execute("UPDATE puzzles SET EncodedURL = ?, Moves = ? WHERE PuzzleId = ?;", [url[2], url[1], url[0]])


if __name__ == '__main__':
    main()

import helpers
import chess
from sqlite3 import Error
import csv


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

    db.commit()
    db.close()


def create_table(db):
    
    try:
        db.execute('CREATE TABLE puzzles("PuzzleId" TEXT, "FEN" TEXT, "Moves" TEXT, "Rating" INTEGER, "Pieces" TEXT);')
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
                    print(f"{reader.line_num} / {num_lines} puzzles imported", end='/r')

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
        
        # Make the first move in the puzzle, remove it from the move list and
        # update the FEN
        moves = moves.split()
        board = chess.Board(original_fen)
        first_move = moves.pop(0)
        move_1 = chess.Move.from_uci(first_move)
        board.push(move_1)
        new_fen = board.fen()
        moves = ' '.join(moves)

        # Update the FEN and move list for the puzzle
        cur.execute("UPDATE puzzles SET FEN = ?, Moves = ? WHERE PuzzleId = ?;", [new_fen, moves, PuzzleId])
        
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

if __name__ == '__main__':
    main()

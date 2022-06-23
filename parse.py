"""This program takes the initally imported puzzle.db and edits the FENs
   to start with the second move in the puzzle. This is done because the
   tactics trainer on the Lichess website makes the first move for you so
   you can see the last move that was made before the tactic."""

from itertools import count
import chess
import helpers

# Create connection to puzzles.db
db = helpers.create_connection("puzzles.db")
cursor = db.cursor()

# Get all of the initial FENs and the moves for each puzzle
original_lines = []
counter = 0

for row in cursor.execute("SELECT PuzzleId, FEN, Moves FROM puzzles;"):
    tmp = []
    tmp.append(row[0])
    tmp.append(row[1])
    tmp.append(row[2])
    original_lines.append(tmp)
    counter += 1
    if counter % 5000 == 0:
        print(f"{counter} lines read")

counter = 0

db.close()
db = helpers.create_connection("puzzles.db")
cursor = db.cursor()

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
    cursor.execute("UPDATE puzzles SET FEN = ?, Moves = ? WHERE PuzzleId = ?;", [new_fen, moves, PuzzleId])
    
    counter += 1
    print(f"{counter} rows updated.")

# Save database changes and close database
db.commit()
db.close()

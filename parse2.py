"""This program creates a new column in puzzles.db that lists the pieces for both the
   player and the opponent in each puzzle. The convention is player pieces will be 
   upper-case and opponent pieces will be lower-case."""

import helpers

# Create connection to puzzles.db
db = helpers.create_connection('puzzles.db')
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

# Save database changes and close database
db.commit()
db.close()

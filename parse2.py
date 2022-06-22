# Create a column containing only the pieces in the FEN

import sqlite3
import helpers

db = helpers.create_connection('puzzles.db')
cur = db.cursor()

pieces = []
fen_list = []
counter = 0

for row in cur.execute("SELECT FEN FROM puzzles;"):
    fen_list.append(row[0])

for fen in fen_list:
    pieces.append('')
    tmp = fen.split(' ')
    print(tmp)
    if tmp[1] == 'b':
        tmp[0] = tmp[0].swapcase()
    for char in tmp[0]:
        if char.isalpha() and char not in pieces[counter] and char not in ['k', 'K']:
            pieces[counter] += char
    pieces[counter] = ''.join(sorted(pieces[counter]))
    cur.execute("UPDATE puzzles SET Pieces = ? WHERE FEN = ?;", [pieces[counter], fen])
    counter += 1
    
db.commit()
db.close()

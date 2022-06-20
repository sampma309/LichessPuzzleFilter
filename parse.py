import csv
import sqlite3
from sqlite3 import Error
import chess
from helpers import create_connection

db = helpers.create_connection("puzzles.db")
cursor = db.cursor()

original_lines = cursor.execute("SELECT PuzzleId, FEN, Moves FROM puzzles;")

for line in original_lines:
    print(line)
    
    PuzzleId = line[0]
    original_fen = line[1]
    moves = line[2]
    
    moves = moves.split()
    board = chess.Board(original_fen)
    first_move = moves.pop(0)
    move_1 = chess.Move.from_uci(first_move)
    board.push(move_1)
    new_fen = board.fen()
    
    print(new_fen)
    print(' '.join(moves))

    moves = ' '.join(moves)

    cursor.execute("UPDATE puzzles SET FEN = ?, Moves = ? WHERE PuzzleId = ?;",
                    [new_fen, moves, PuzzleId])

db.commit()
db.close()

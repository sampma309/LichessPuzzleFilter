import chess
import base64

board = chess.Board("r1bqk2r/pp1nbNp1/2p1p2p/8/2BP4/1PN3P1/P3QP1P/3R1RK1 b kq - 0 19")
# moves = [f2g3 e6e7 b2b1 b3c1 b1c1 h6c1]

moves = 'e8f7 e2e6 f7f8 e6f7'


moves = moves.split()
first_move = moves.pop(0)
move_1 = chess.Move.from_uci(first_move)
board.push(move_1)
print(board.fen())
fen = board.fen()
#variation = board.variation_san([chess.Move.from_uci(move) for move in moves])
variation = []
last_move = moves[-1]
while moves:
    move = moves.pop(0)
    variation.append(board.san(chess.Move.from_uci(move)))
    move_on_board = chess.Move.from_uci(move)
    board.push(move_on_board)


print(*variation, sep=' ')
variation = ' '.join(variation)
print(variation)
print(last_move)
encode_string = f"{fen};{variation};{last_move}"
print(encode_string)
listudy_encode = base64.standard_b64encode(encode_string.encode())
print(listudy_encode)


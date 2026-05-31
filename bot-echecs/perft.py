from board import Bitboard
from move_generation import generate_legal_moves

def perft(board, depth, color):
    if depth == 0:
        return 1

    nodes = 0

    moves = generate_legal_moves(board, color)

    for move in moves:
        undo = board.make_move(move)

        nodes += perft(board, depth - 1, not color)

        board.unmake_move(move, undo)

    return nodes

if __name__ == "__main__":
    board = Bitboard("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
    print(perft(board, 3, True))  # True for white to move
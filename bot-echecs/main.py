from board import Bitboard
from move_generation import generate_legal_moves
from move_searching import select_move
import sys
import time

def main():
    # Usage: python main.py "<FEN>" [max_seconds]
    fen = None
    max_seconds = 10.0
    args = sys.argv[1:]
    if len(args) >= 1:
        fen = args[0]
    if len(args) >= 2:
        try:
            max_seconds = float(args[1])
        except Exception:
            pass

    board = Bitboard(fen) if fen else Bitboard()

    deadline = time.time() + max_seconds
    best_move = None
    depth = 1

    # Iterative deepening: increase depth until time runs out or a depth cap
    while True:
        move = select_move(board, depth, deadline=deadline)

        # If search returned a move, update best_move
        if move is not None:
            best_move = move
        else:
            break

        depth += 1
        if depth > 20:
            break

    if best_move:
        print(best_move.lan()) 
    else:
        print("No move found")

if __name__ == "__main__":
    main()

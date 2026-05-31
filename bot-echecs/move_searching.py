from board import Bitboard
from move import Move
from move_generation import generate_legal_moves, is_in_check
from evaluation import evaluate, pawnvalue, knightvalue, bishopvalue, rookvalue, queenvalue, kingvalue
from constants import (
    pawns_table,
    knights_table,
    bishops_table,
    rooks_table,
    queens_table,
    king_early_table,
    king_late_table,
    black_pawns_table,
    black_knights_table,
    black_bishops_table,
    black_rooks_table,
    black_queens_table,
    black_king_early_table,
    black_king_late_table,
)
from helpers import hamming_weight
import os
import random
import re
from typing import List

PIECE_VALUES = {
    "p": pawnvalue,
    "n": knightvalue,
    "b": bishopvalue,
    "r": rookvalue,
    "q": queenvalue,
    "k": kingvalue,
}

def has_queen_and_limited_support(bitboard: Bitboard, white: bool) -> bool:
    side_mask = bitboard.white_pieces if white else bitboard.black_pieces
    queen_count = hamming_weight(bitboard.queens & side_mask)
    if queen_count == 0:
        return True

    support_mask = bitboard.knights | bitboard.bishops | bitboard.rooks
    support_count = hamming_weight(support_mask & side_mask)
    return support_count <= 1


def use_late_king_table(bitboard: Bitboard) -> bool:
    white_ok = has_queen_and_limited_support(bitboard, True)
    black_ok = has_queen_and_limited_support(bitboard, False)
    return white_ok and black_ok


def piece_square_table(piece: str, white: bool, use_late_king: bool = False) -> list[int] | None:
    if piece == "p":
        return pawns_table if white else black_pawns_table
    if piece == "n":
        return knights_table if white else black_knights_table
    if piece == "b":
        return bishops_table if white else black_bishops_table
    if piece == "r":
        return rooks_table if white else black_rooks_table
    if piece == "q":
        return queens_table if white else black_queens_table
    if piece == "k":
        if use_late_king:
            return king_late_table if white else black_king_late_table
        return king_early_table if white else black_king_early_table
    return None


def pawn_attack_mask(pawns: int, by_white: bool) -> int:
    not_a_file = 0xfefefefefefefefe
    not_h_file = 0x7f7f7f7f7f7f7f7f

    if by_white:
        return ((pawns & not_a_file) << 7) | ((pawns & not_h_file) << 9)

    return ((pawns & not_h_file) >> 7) | ((pawns & not_a_file) >> 9)

def move_order_score(bitboard: Bitboard, move: Move, pawn_threat_mask: int) -> int:
    score = 0
    mover_piece = bitboard.get_piece_at(move.from_sq)

    # Captures
    captured_piece = None
    if move.is_en_passant:
        captured_piece = "p"
    else:
        captured_piece = bitboard.get_piece_at(move.to_sq)

    if captured_piece:
        captured_value = PIECE_VALUES.get(captured_piece, 0)
        attacker_value = PIECE_VALUES.get(mover_piece, 0)

        score = captured_value - attacker_value

    # Promotion bonus
    if move.promotion:
        score += PIECE_VALUES.get(move.promotion, 0)

    # Discourage moving into pawn attacks
    if pawn_threat_mask & (1 << move.to_sq):
        score -= PIECE_VALUES.get(mover_piece, 0)

    return score

def order_moves(bitboard: Bitboard, moves: list[Move]) -> list[Move]:
    enemy_color = not bitboard.active_color
    enemy_pawns = bitboard.pawns & (bitboard.black_pieces if enemy_color else bitboard.white_pieces)
    pawn_threat_mask = pawn_attack_mask(enemy_pawns, by_white=enemy_color)

    return sorted(
        moves,
        key=lambda move: move_order_score(bitboard, move, pawn_threat_mask),
        reverse=True,
    )

def searchAllCaptures(bitboard: Bitboard, alpha: int, beta: int) -> int:
    evaluation = evaluate(bitboard)
    if evaluation >= beta:
        return beta
    
    alpha = max(alpha, evaluation)
    moves = order_moves(bitboard, generate_legal_moves(bitboard, bitboard.active_color, only_captures=True))

    for move in moves:
        undo = bitboard.make_move(move)

        score = -searchAllCaptures(bitboard, -beta, -alpha)

        bitboard.unmake_move(move, undo)

        if score >= beta:
            return beta
        alpha = max(alpha, score)
    
    return alpha

def search(bitboard : Bitboard, depth : int, alpha : int, beta : int) -> int:
    if depth == 0:
        return searchAllCaptures(bitboard, alpha, beta)
    
    moves = order_moves(bitboard, generate_legal_moves(bitboard, bitboard.active_color))

    # Checkmate or stalemate
    if len(moves) == 0:
        if is_in_check(bitboard, bitboard.active_color):
            return -99999
        return 0
    
    for move in moves:
        undo = bitboard.make_move(move)

        score = -search(bitboard, depth - 1, -beta, -alpha)

        bitboard.unmake_move(move, undo)

        if score >= beta:
            return beta
        alpha = max(alpha, score)

    return alpha


def _parse_uci_move(token: str, board: Bitboard) -> Move | None:
    """
    Parse a SAN move token into a Move by comparing to generated legal moves' SAN.
    """
    if not token:
        return None

    token = token.strip()

    # ignore game result tokens and move-number tokens
    if token in ("1-0", "0-1", "1/2-1/2"):
        return None
    if token.endswith('.') or token.isdigit():
        return None

    def normalize(s: str) -> str:
        s = s.replace('0', 'O')
        s = s.strip()
        s = re.sub(r'[!?+#]+$', '', s)
        return s

    norm_token = normalize(token)

    legal = generate_legal_moves(board, board.active_color)

    for m in legal:
        try:
            san = m.san(board, legal)
        except Exception:
            san = m.san(board, None)

        if normalize(san) == norm_token:
            return m

    return None


def _boards_equal(a: Bitboard, b: Bitboard) -> bool:
    return (
        a.pawns == b.pawns
        and a.knights == b.knights
        and a.bishops == b.bishops
        and a.rooks == b.rooks
        and a.queens == b.queens
        and a.kings == b.kings
        and a.white_pieces == b.white_pieces
        and a.black_pieces == b.black_pieces
        and a.active_color == b.active_color
    )


def _load_games(path: str) -> List[List[str]]:
    """Load games from a file. Each line is expected to be a sequence of UCI-style moves separated by whitespace.
    Empty lines and lines starting with '#' are ignored.
    """
    games: List[List[str]] = []
    if not os.path.exists(path):
        return games

    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            tokens = s.split()
            games.append(tokens)

    return games


def get_book_move(bitboard: Bitboard, games_path: str = 'Games.txt') -> Move | None:
    """
    If the current position appears in one of the games within the first five ply (moves),
    return the next book move as a `Move` object. If this is the initial position, randomly pick
    one game's first move.
    Games file format: one game per line, moves in UCI/coordinate format (e.g. e2e4 e7e5 g1f3 ...).
    """
    games = _load_games(games_path)
    if not games:
        return None

    # If this is the initial position (no moves played), pick a random game's first move
    initial_board = Bitboard()
    if _boards_equal(initial_board, bitboard):
        # pick random game that has at least one move and return its first move if legal
        choices = [g for g in games if len(g) >= 1]
        if not choices:
            return None
        game = random.choice(choices)
        move = _parse_uci_move(game[0], initial_board)
        if move:
            # only return if the move is legal in current position
            legal = generate_legal_moves(bitboard, bitboard.active_color)
            for m in legal:
                if m.from_sq == move.from_sq and m.to_sq == move.to_sq and m.promotion == move.promotion:
                    return m
        return None

    # Otherwise, try to find the current position in the first five moves of any game
    for game in games:
        board = Bitboard()
        max_ply = min(len(game), 10)  # first five full moves -> 10 ply
        for ply_index in range(max_ply):
            token = game[ply_index]
            parsed = _parse_uci_move(token, board)
            if parsed is None:
                break

            # If the board matches the target before making this move, return this move
            if _boards_equal(board, bitboard):
                legal = generate_legal_moves(board, board.active_color)
                for m in legal:
                    if m.from_sq == parsed.from_sq and m.to_sq == parsed.to_sq and m.promotion == parsed.promotion:
                        return m

            # Play the token move on the running board if legal
            legal = generate_legal_moves(board, board.active_color)
            matched = False
            for m in legal:
                if m.from_sq == parsed.from_sq and m.to_sq == parsed.to_sq and m.promotion == parsed.promotion:
                    board.make_move(m)
                    matched = True
                    break
            if not matched:
                break

        # After replaying up to max_ply, check if final position equals our board and there's a next move
        if _boards_equal(board, bitboard):
            next_index = max_ply
            if next_index < len(game):
                next_parsed = _parse_uci_move(game[next_index], board)
                if next_parsed:
                    legal = generate_legal_moves(board, board.active_color)
                    for m in legal:
                        if m.from_sq == next_parsed.from_sq and m.to_sq == next_parsed.to_sq and m.promotion == next_parsed.promotion:
                            return m

    return None


def select_move(bitboard: Bitboard, depth: int, alpha: int = -99999, beta: int = 99999) -> Move | None:
    """
    Tries book move first (within first five moves of games),
    otherwise runs an alpha-beta search and returns the best Move.
    """
    legal_moves = generate_legal_moves(bitboard, bitboard.active_color)
    if not legal_moves:
        return None

    # Try book
    book_move = get_book_move(bitboard)
    if book_move is not None:
        # ensure it's legal in current position
        for m in legal_moves:
            if m.from_sq == book_move.from_sq and m.to_sq == book_move.to_sq and m.promotion == book_move.promotion:
                return m

    # Fall back to search: iterate moves and pick best score
    best_score = -999999
    best_move: Move | None = None
    ordered = order_moves(bitboard, legal_moves)
    for move in ordered:
        undo = bitboard.make_move(move)
        score = -search(bitboard, depth - 1, -beta, -alpha)
        bitboard.unmake_move(move, undo)

        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_move
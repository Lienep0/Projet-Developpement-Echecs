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

def select_move(bitboard: Bitboard, depth: int, alpha: int = -99999, beta: int = 99999) -> Move | None:
    """
    Tries book move first (within first five moves of games),
    otherwise runs an alpha-beta search and returns the best Move.
    """
    legal_moves = generate_legal_moves(bitboard, bitboard.active_color)
    if not legal_moves:
        return None

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

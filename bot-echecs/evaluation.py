from board import Bitboard
from helpers import hamming_weight
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

pawnvalue = 100
knightvalue = 320
bishopvalue = 330
rookvalue = 500
queenvalue = 900
kingvalue = 20000


def bitscan(bbm: int):
    while bbm:
        lsb = bbm & -bbm
        sq = (lsb.bit_length() - 1)
        yield sq
        bbm ^= lsb


def has_queen_and_limited_support(bitboard: Bitboard, white: bool) -> bool:
    side_mask = bitboard.white_pieces if white else bitboard.black_pieces
    queen_count = hamming_weight(bitboard.queens & side_mask)
    if queen_count == 0:
        return True

    support_mask = bitboard.knights | bitboard.bishops | bitboard.rooks
    support_count = hamming_weight(support_mask & side_mask)
    return support_count <= 1


def evaluate(bitboard: Bitboard) -> int:
    """Evaluate material + piece-square tables. Returns score from side-to-move perspective."""
    white_material = 0
    black_material = 0

    # Material
    white_material += hamming_weight(bitboard.pawns & bitboard.white_pieces) * pawnvalue
    white_material += hamming_weight(bitboard.knights & bitboard.white_pieces) * knightvalue
    white_material += hamming_weight(bitboard.bishops & bitboard.white_pieces) * bishopvalue
    white_material += hamming_weight(bitboard.rooks & bitboard.white_pieces) * rookvalue
    white_material += hamming_weight(bitboard.queens & bitboard.white_pieces) * queenvalue

    black_material += hamming_weight(bitboard.pawns & bitboard.black_pieces) * pawnvalue
    black_material += hamming_weight(bitboard.knights & bitboard.black_pieces) * knightvalue
    black_material += hamming_weight(bitboard.bishops & bitboard.black_pieces) * bishopvalue
    black_material += hamming_weight(bitboard.rooks & bitboard.black_pieces) * rookvalue
    black_material += hamming_weight(bitboard.queens & bitboard.black_pieces) * queenvalue

    # Piece-square table contributions
    white_pst = 0
    black_pst = 0

    use_late = (has_queen_and_limited_support(bitboard, True) and has_queen_and_limited_support(bitboard, False))

    # Pawns
    for sq in bitscan(bitboard.pawns & bitboard.white_pieces):
        white_pst += pawns_table[sq]
    for sq in bitscan(bitboard.pawns & bitboard.black_pieces):
        black_pst += black_pawns_table[sq]

    # Knights
    for sq in bitscan(bitboard.knights & bitboard.white_pieces):
        white_pst += knights_table[sq]
    for sq in bitscan(bitboard.knights & bitboard.black_pieces):
        black_pst += black_knights_table[sq]

    # Bishops
    for sq in bitscan(bitboard.bishops & bitboard.white_pieces):
        white_pst += bishops_table[sq]
    for sq in bitscan(bitboard.bishops & bitboard.black_pieces):
        black_pst += black_bishops_table[sq]

    # Rooks
    for sq in bitscan(bitboard.rooks & bitboard.white_pieces):
        white_pst += rooks_table[sq]
    for sq in bitscan(bitboard.rooks & bitboard.black_pieces):
        black_pst += black_rooks_table[sq]

    # Queens
    for sq in bitscan(bitboard.queens & bitboard.white_pieces):
        white_pst += queens_table[sq]
    for sq in bitscan(bitboard.queens & bitboard.black_pieces):
        black_pst += black_queens_table[sq]

    # Kings (choose early/late table)
    king_table_w = king_late_table if use_late else king_early_table
    king_table_b = black_king_late_table if use_late else black_king_early_table
    for sq in bitscan(bitboard.kings & bitboard.white_pieces):
        white_pst += king_table_w[sq]
    for sq in bitscan(bitboard.kings & bitboard.black_pieces):
        black_pst += king_table_b[sq]

    white_total = white_material + white_pst
    black_total = black_material + black_pst

    evaluation = white_total - black_total
    perspective = 1 if bitboard.active_color else -1
    return evaluation * perspective

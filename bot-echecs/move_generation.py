from typing import Iterator
from constants import *
from move import Move
from board import Bitboard

def bitscan(bbm : int) -> Iterator[int]:
    """
    Helper to extract squares from a bitboard mask.
    Generates an iterator that gives all the indexes of the occupied bb squares.
    """
    while bbm:
        lsb = bbm & -bbm
        sq = (lsb.bit_length() - 1)
        yield sq
        bbm ^= lsb

def generate_pawn_moves(bitboard : Bitboard, color : bool) -> list[Move]:
    """
    Generate pseudo-legal pawn moves for the given color.

    bitboard: the current bitboard representation of the board
    color : white is True, black is False
    """
    moves = []

    # Bitboard masks
    own = bitboard.white_pieces if color else bitboard.black_pieces
    opponent = bitboard.black_pieces if color else bitboard.white_pieces
    pawns = bitboard.pawns & own
    occupied = bitboard.white_pieces | bitboard.black_pieces
    empty = ~occupied & 0xFFFFFFFFFFFFFFFF
    
    # File masks to prevent wrap-around
    not_a_file = 0xfefefefefefefefe
    not_h_file = 0x7f7f7f7f7f7f7f7f

    promotion_rank = range(56, 64) if color else range(0, 8)

    def append_move(from_sq: int, to_sq: int, **kwargs):
        if to_sq in promotion_rank:
            for promotion in ["q", "r", "b", "n"]:
                moves.append(Move(from_sq, to_sq, promotion=promotion, **kwargs))
        else:
            moves.append(Move(from_sq, to_sq, **kwargs))
    
    if color:
        # Single pushes
        single_push = (pawns << 8) & empty
        # Double pushes from rank 2
        rank2 = 0x000000000000FF00
        double_push = ((pawns & rank2) << 16) & empty & ((empty) << 8)
        # Captures
        capture_left  = ((pawns & not_a_file) << 7) & opponent
        capture_right = ((pawns & not_h_file) << 9) & opponent
        shift = 8  # for reversing single pushes
    else:
        # Black pawns move down
        single_push = (pawns >> 8) & empty
        rank7 = 0x00FF000000000000
        double_push = ((pawns & rank7) >> 16) & empty & ((empty) >> 8)
        capture_left  = ((pawns & not_a_file) >> 9) & opponent
        capture_right = ((pawns & not_h_file) >> 7) & opponent
        shift = -8  # for reversing single pushes

    # Single pushes
    for to_sq in bitscan(single_push):
        from_sq = to_sq - shift
        append_move(from_sq, to_sq)

    # Double pushes
    for to_sq in bitscan(double_push):
        from_sq = to_sq - shift * 2
        append_move(from_sq, to_sq, is_double_push=True)

    # Captures left
    cap_shift = 7 if color else -9
    for to_sq in bitscan(capture_left):
        from_sq = to_sq - cap_shift
        append_move(from_sq, to_sq)

    # Captures right
    cap_shift = 9 if color else -7
    for to_sq in bitscan(capture_right):
        from_sq = to_sq - cap_shift
        append_move(from_sq, to_sq)

    # En passant
    if bitboard.en_passant != -1:
        ep_mask = 1 << bitboard.en_passant

        if color:
            ep_left = ((pawns & not_a_file) << 7) & ep_mask
            ep_right = ((pawns & not_h_file) << 9) & ep_mask

            for to_sq in bitscan(ep_left):
                append_move(to_sq - 7, to_sq, is_en_passant=True)

            for to_sq in bitscan(ep_right):
                append_move(to_sq - 9, to_sq, is_en_passant=True)
        else:
            ep_left = ((pawns & not_a_file) >> 9) & ep_mask
            ep_right = ((pawns & not_h_file) >> 7) & ep_mask

            for to_sq in bitscan(ep_left):
                append_move(to_sq + 9, to_sq, is_en_passant=True)

            for to_sq in bitscan(ep_right):
                append_move(to_sq + 7, to_sq, is_en_passant=True)

    return moves

def generate_knight_moves(bitboard : Bitboard, color : bool) -> list[Move]:
    """
    Generate pseudo-legal knight moves for the given color.
    
    bitboard: the current bitboard representation of the board
    color : white is True, black is False
    """
    moves = []

    own = bitboard.white_pieces if color else bitboard.black_pieces
    knights = bitboard.knights & own

    while knights:
        lsb = knights & -knights
        from_sq = lsb.bit_length() - 1
        knights ^= lsb

        attacks = knight_masks[from_sq] & ~own

        for to_sq in bitscan(attacks):
            moves.append(Move(from_sq, to_sq))

    return moves

def generate_king_moves(bitboard: Bitboard, color: bool) -> list[Move]:
    """
    Generate pseudo-legal king moves for the given color.
    
    bitboard: the current bitboard representation of the board
    color : white is True, black is False
    """
    moves = []

    own = bitboard.white_pieces if color else bitboard.black_pieces
    opponent = bitboard.black_pieces if color else bitboard.white_pieces

    occupied = own | opponent

    kings = bitboard.kings & own

    if not kings:
        return moves

    from_sq = (kings & -kings).bit_length() - 1

    attacks = king_masks[from_sq] & ~own

    for to_sq in bitscan(attacks):
        moves.append(Move(from_sq, to_sq))

    # Castling
    if color:

        # White kingside
        if bitboard.white_can_castle_kingside:
            if not (occupied & ((1 << 5) | (1 << 6))):
                if not is_square_attacked(bitboard, 4, by_white=False) and not is_square_attacked(bitboard, 5, by_white=False) and not is_square_attacked(bitboard, 6, by_white=False):
                    moves.append(Move(4, 6, is_castling=True))

        # White queenside
        if bitboard.white_can_castle_queenside:
            if not (occupied & ((1 << 1) | (1 << 2) | (1 << 3))):
                if not is_square_attacked(bitboard, 4, by_white=False) and not is_square_attacked(bitboard, 3, by_white=False) and not is_square_attacked(bitboard, 2, by_white=False):
                    moves.append(Move(4, 2, is_castling=True))
    else:

        # Black kingside
        if bitboard.black_can_castle_kingside:
            if not (occupied & ((1 << 61) | (1 << 62))):
                if not is_square_attacked(bitboard, 60, by_white=True) and not is_square_attacked(bitboard, 61, by_white=True) and not is_square_attacked(bitboard, 62, by_white=True):
                    moves.append(Move(60, 62, is_castling=True))

        # Black queenside
        if bitboard.black_can_castle_queenside:
            if not (occupied & ((1 << 57) | (1 << 58) | (1 << 59))):
                if not is_square_attacked(bitboard, 60, by_white=True) and not is_square_attacked(bitboard, 59, by_white=True) and not is_square_attacked(bitboard, 58, by_white=True):
                    moves.append(Move(60, 58, is_castling=True))
    return moves

def generate_sliding_moves(bitboard : Bitboard, color : bool, piece_type : int) -> list[Move]:
    """
    Generate pseudo-legal sliding piece moves for the given color.
    
    bitboard: the current bitboard representation of the board
    color: white is True, black is False
    piece_type: 0 is Bishops, 1 is Rooks, 2 is Queens, 3 is Kings
    """
    moves = []

    match piece_type:
        case 0:
            direction_rays = [northwest_rays, northeast_rays, southwest_rays, southeast_rays]
            piece_mask = bitboard.bishops
        case 1:
            direction_rays = [north_rays, south_rays, west_rays, east_rays]
            piece_mask = bitboard.rooks
        case _:
            direction_rays = [
                north_rays, south_rays, west_rays, east_rays,
                northwest_rays, northeast_rays, southwest_rays, southeast_rays
            ]
            piece_mask = bitboard.queens

    own = bitboard.white_pieces if color else bitboard.black_pieces
    opponent = bitboard.black_pieces if color else bitboard.white_pieces
    pieces = piece_mask & own

    while pieces:
        lsb = pieces & -pieces
        from_sq = lsb.bit_length() - 1
        pieces ^= lsb

        for ray in direction_rays:
            for to_sq in ray[from_sq]:

                if own & (1 << to_sq):
                    break

                moves.append(Move(from_sq, to_sq))

                if opponent & (1 << to_sq):
                    break

    return moves

def generate_pseudolegal_moves(bitboard : Bitboard, color : bool) -> list[Move]:
    return ( 
        generate_pawn_moves(bitboard, color) 
        + generate_knight_moves(bitboard, color)
        + generate_sliding_moves(bitboard, color, 0) # Bishops
        + generate_sliding_moves(bitboard, color, 1) # Rooks
        + generate_sliding_moves(bitboard, color, 2) # Queens
        + generate_king_moves(bitboard, color) # Kings
    )


def is_square_attacked(bitboard: Bitboard, square: int, by_white: bool) -> bool:
    """Return True if `square` is attacked by the given color."""
    not_a_file = 0xfefefefefefefefe
    not_h_file = 0x7f7f7f7f7f7f7f7f
    occupied = bitboard.white_pieces | bitboard.black_pieces

    attackers = bitboard.white_pieces if by_white else bitboard.black_pieces
    pawns = bitboard.pawns & attackers
    knights = bitboard.knights & attackers
    bishops = bitboard.bishops & attackers
    rooks = bitboard.rooks & attackers
    queens = bitboard.queens & attackers
    kings = bitboard.kings & attackers

    # Pawn attacks
    if by_white:
        if square >= 7 and (not_a_file & (1 << (square - 7))) and (pawns & (1 << (square - 7))):
            return True
        if square >= 9 and (not_h_file & (1 << (square - 9))) and (pawns & (1 << (square - 9))):
            return True
    else:
        if square <= 56 and (not_h_file & (1 << (square + 7))) and (pawns & (1 << (square + 7))):
            return True
        if square <= 55 and (not_a_file & (1 << (square + 9))) and (pawns & (1 << (square + 9))):
            return True

    # Knight attacks
    if knight_masks[square] & knights:
        return True

    # King attacks
    if king_masks[square] & kings:
        return True

    # Sliding attacks - rooks and queens on orthogonal rays
    for ray in (north_rays, south_rays, east_rays, west_rays):
        for target in ray[square]:
            target_mask = 1 << target
            if occupied & target_mask:
                if rooks & target_mask or queens & target_mask:
                    return True
                break

    # Sliding attacks - bishops and queens on diagonal rays
    for ray in (northwest_rays, northeast_rays, southwest_rays, southeast_rays):
        for target in ray[square]:
            target_mask = 1 << target
            if occupied & target_mask:
                if bishops & target_mask or queens & target_mask:
                    return True
                break

    return False


def is_in_check(bitboard: Bitboard, color: bool) -> bool:
    """Return True if the side `color` is currently in check."""
    king_bb = bitboard.kings & (bitboard.white_pieces if color else bitboard.black_pieces)
    if not king_bb:
        return False

    king_square = (king_bb & -king_bb).bit_length() - 1
    return is_square_attacked(bitboard, king_square, by_white=not color)


def generate_legal_moves(bitboard, color, only_captures=False) -> list[Move]:
    legal_moves = []

    pseudo_moves = generate_pseudolegal_moves(bitboard, color)

    for move in pseudo_moves:
        undo = bitboard.make_move(move)

        # A legal move must not leave the moving side in check
        if not is_in_check(bitboard, color):
            legal_moves.append(move)

        bitboard.unmake_move(move, undo)

    if only_captures:
        legal_moves = [move for move in legal_moves if move.is_en_passant or bitboard.get_piece_at(move.to_sq) is not None]

    return legal_moves
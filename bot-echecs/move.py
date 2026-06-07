from dataclasses import dataclass
from typing import Any

@dataclass
class Move:
    """
    Represents a move from from_sq to to_sq, with optional promotion and flags for special move types
    """

    from_sq: int
    to_sq: int
    promotion: str | None = None
    is_en_passant: bool = False
    is_castling: bool = False
    is_double_push: bool = False

    def san(self, board: Any, legal_moves: list['Move'] | None = None) -> str:
        """Return standard algebraic notation for this move."""
        return move_to_san(self, board, legal_moves)
        
    def lan(self) -> str:
        """Return UCI for this move"""
        start = square_name(self.from_sq)
        end = square_name(self.to_sq)
        promo = self.promotion.lower() if self.promotion else ""
        return f"{start}{end}{promo}"

@dataclass
class Undo:
    """
    Represents a potential undo of a move
    """
    moved_piece: str | None
    captured_piece: str | None

    previous_en_passant: int

    white_ks: bool
    white_qs: bool
    black_ks: bool
    black_qs: bool


def square_name(square: int) -> str:
    file = square % 8
    rank = square // 8
    return f"{chr(ord('a') + file)}{rank + 1}"


def piece_symbol(piece: str | None) -> str:
    if piece is None or piece == "p":
        return ""
    return piece.upper()


def move_to_san(move: Move, board: Any, legal_moves: list[Move] | None = None) -> str:
    if move.is_castling:
        return "O-O" if move.to_sq in (6, 62) else "O-O-O"

    if legal_moves is None:
        from move_generation import generate_legal_moves

        legal_moves = generate_legal_moves(board, board.active_color)

    piece = board.get_piece_at(move.from_sq)
    if piece is None:
        raise ValueError(f"No piece found on square {move.from_sq}")

    is_capture = move.is_en_passant or board.get_piece_at(move.to_sq) is not None
    destination = square_name(move.to_sq)
    promotion = f"={move.promotion.upper()}" if move.promotion else ""

    symbol = piece_symbol(piece)
    disambiguation = ""

    if symbol:
        same_piece_moves = [other for other in legal_moves
                            if other != move
                            and other.to_sq == move.to_sq
                            and board.get_piece_at(other.from_sq) == piece]

        if same_piece_moves:
            from_file = chr(ord('a') + (move.from_sq % 8))
            from_rank = str((move.from_sq // 8) + 1)
            same_file = any((other.from_sq % 8) == (move.from_sq % 8) for other in same_piece_moves)
            same_rank = any((other.from_sq // 8) == (move.from_sq // 8) for other in same_piece_moves)

            if same_file and same_rank:
                disambiguation = f"{from_file}{from_rank}"
            elif same_file:
                disambiguation = from_rank
            elif same_rank:
                disambiguation = from_file
            else:
                disambiguation = from_file

    if not symbol:
        if is_capture:
            from_file = chr(ord('a') + (move.from_sq % 8))
            return f"{from_file}x{destination}{promotion}"
        return f"{destination}{promotion}"

    capture_text = "x" if is_capture else ""
    san = f"{symbol}{disambiguation}{capture_text}{destination}{promotion}"

    from move_generation import generate_legal_moves, is_in_check

    undo = board.make_move(move)
    try:
        if is_in_check(board, board.active_color):
            suffix = "+"
            if not generate_legal_moves(board, board.active_color):
                suffix = "#"
        else:
            suffix = ""
    finally:
        board.unmake_move(move, undo)

    return san + suffix

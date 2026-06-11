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
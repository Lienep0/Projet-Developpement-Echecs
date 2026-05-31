from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from move import Move, Undo

class Bitboard:
    """
    Represents a Bitboard, which is a representation
    of a chess board using bit masks.
    Each piece has its positions represented by a bitmask,
    and each color has a bitmask too.
    """

    def __init__(self, FEN : str = None) -> 'Bitboard':
        if FEN:
            self.init_from_FEN(FEN.strip())
        else:
            # Default chess starting position
            self.pawns   = 0b0000000011111111000000000000000000000000000000001111111100000000
            self.rooks   = 0b1000000100000000000000000000000000000000000000000000000010000001
            self.knights = 0b0100001000000000000000000000000000000000000000000000000001000010
            self.bishops = 0b0010010000000000000000000000000000000000000000000000000000100100
            self.queens  = 0b0000100000000000000000000000000000000000000000000000000000001000
            self.kings   = 0b0001000000000000000000000000000000000000000000000000000000010000

            self.white_pieces = 0b0000000000000000000000000000000000000000000000001111111111111111
            self.black_pieces = 0b1111111111111111000000000000000000000000000000000000000000000000

            # White to move
            self.active_color = True
            self.en_passant = -1

            # Castling 
            self.white_can_castle_kingside = True
            self.white_can_castle_queenside = True
            self.black_can_castle_kingside = True
            self.black_can_castle_queenside = True

    def make_move(self, move: 'Move') -> 'Undo':
        """
        Makes a move from a Move object and updates the active color
        Returns an undo object to be used if the move needs to be undone
        """
        from move import Undo

        piece = self.get_piece_at(move.from_sq)
        captured_piece = self.get_piece_at(move.to_sq)
        if move.is_en_passant:
            capture_sq = move.to_sq - 8 if bool(self.white_pieces & (1 << move.from_sq)) else move.to_sq + 8
            captured_piece = self.get_piece_at(capture_sq)

        undo = Undo(
            moved_piece=piece,
            captured_piece=captured_piece,

            previous_en_passant=self.en_passant,

            white_ks=self.white_can_castle_kingside,
            white_qs=self.white_can_castle_queenside,
            black_ks=self.black_can_castle_kingside,
            black_qs=self.black_can_castle_queenside
        )
        color = bool(self.white_pieces & (1 << move.from_sq))

        # Update castling rights when kings or rooks move or are captured.
        if piece == "k":
            if color:
                self.white_can_castle_kingside = False
                self.white_can_castle_queenside = False
            else:
                self.black_can_castle_kingside = False
                self.black_can_castle_queenside = False
        elif piece == "r":
            if color:
                if move.from_sq == 0:
                    self.white_can_castle_queenside = False
                elif move.from_sq == 7:
                    self.white_can_castle_kingside = False
            else:
                if move.from_sq == 56:
                    self.black_can_castle_queenside = False
                elif move.from_sq == 63:
                    self.black_can_castle_kingside = False

        if captured_piece == "r":
            if color:
                if move.is_en_passant:
                    pass
                elif move.to_sq == 56:
                    self.black_can_castle_queenside = False
                elif move.to_sq == 63:
                    self.black_can_castle_kingside = False
            else:
                if move.is_en_passant:
                    pass
                elif move.to_sq == 0:
                    self.white_can_castle_queenside = False
                elif move.to_sq == 7:
                    self.white_can_castle_kingside = False

        self.remove_piece(move.from_sq)

        # Remove captured piece
        if undo.captured_piece:
            self.remove_piece(move.to_sq)

        # Special en passant case
        if move.is_en_passant:
            if color:
                capture_sq = move.to_sq - 8
            else:
                capture_sq = move.to_sq + 8

            self.remove_piece(capture_sq)

        # Special castling case
        if move.is_castling:
            if move.to_sq == 6:
                self.remove_piece(7)
                self.place_piece(5, "r", True)

            elif move.to_sq == 2:
                self.remove_piece(0)
                self.place_piece(3, "r", True)

            elif move.to_sq == 62:
                self.remove_piece(63)
                self.place_piece(61, "r", False)

            elif move.to_sq == 58:
                self.remove_piece(56)
                self.place_piece(59, "r", False)

        # Promotion
        if move.promotion:
            self.place_piece(move.to_sq, move.promotion, color)
        else:
            self.place_piece(move.to_sq, piece, color)

        # Update en passant state
        self.en_passant = -1
        if move.is_double_push:
            if color:
                self.en_passant = move.to_sq - 8
            else:
                self.en_passant = move.to_sq + 8

        # Toggle side
        self.active_color = not self.active_color

        return undo

    def unmake_move(self, move: 'Move', undo: 'Undo'):
        """
        Restores a board to its original state from a move, and the move's undo object
        Also changes the active color
        """

        # Restore castling rights
        self.white_can_castle_kingside  = undo.white_ks
        self.white_can_castle_queenside = undo.white_qs
        self.black_can_castle_kingside  = undo.black_ks
        self.black_can_castle_queenside = undo.black_qs

        # Restore en passant square
        self.en_passant = undo.previous_en_passant

        color = (self.white_pieces & (1 << move.to_sq)) != 0

        # Undo castling
        if move.is_castling:
            # White kingside
            if move.to_sq == 6:
                self.remove_piece(5)
                self.place_piece(7, "r", True)

            # White queenside
            elif move.to_sq == 2:
                self.remove_piece(3)
                self.place_piece(0, "r", True)

            # Black kingside
            elif move.to_sq == 62:
                self.remove_piece(61)
                self.place_piece(63, "r", False)

            # Black queenside
            elif move.to_sq == 58:
                self.remove_piece(59)
                self.place_piece(56, "r", False)

        # Undo main move
        self.remove_piece(move.to_sq)
        self.place_piece(move.from_sq, undo.moved_piece, color)

        # Undo capture
        if undo.captured_piece:
            # En passant capture special case
            if move.is_en_passant:
                if color:
                    cap_sq = move.to_sq - 8
                else:
                    cap_sq = move.to_sq + 8
            else:
                cap_sq = move.to_sq

            cap_color = not color
            self.place_piece(cap_sq, undo.captured_piece, cap_color)

        # Undo promotion
        if move.promotion:
            self.remove_piece(move.from_sq)
            self.place_piece(move.from_sq, "p", color)

        # Toggle side
        self.active_color = not self.active_color

    def get_piece_at(self, square):
        mask = 1 << square

        if self.pawns & mask:
            return "p"
        if self.knights & mask:
            return "n"
        if self.bishops & mask:
            return "b"
        if self.rooks & mask:
            return "r"
        if self.queens & mask:
            return "q"
        if self.kings & mask:
            return "k"

        return None

    def remove_piece(self, square):
        mask = ~(1 << square)

        self.pawns &= mask
        self.knights &= mask
        self.bishops &= mask
        self.rooks &= mask
        self.queens &= mask
        self.kings &= mask

        self.white_pieces &= mask
        self.black_pieces &= mask

    def place_piece(self, square, piece, white):
        mask = 1 << square

        match piece:
            case "p":
                self.pawns |= mask
            case "n":
                self.knights |= mask
            case "b":
                self.bishops |= mask
            case "r":
                self.rooks |= mask
            case "q":
                self.queens |= mask
            case "k":
                self.kings |= mask

        if white:
            self.white_pieces |= mask
        else:
            self.black_pieces |= mask

    def init_from_FEN(self, FEN : str):
        parts = FEN.split(' ')

        board_part = parts[0]
        active_color = parts[1]
        castling = parts[2]
        en_passant = parts[3]
        halfmove = int(parts[4])
        fullmove = int(parts[5])

        self.active_color = active_color == 'w'
        self.en_passant = self.square_to_index(en_passant) if en_passant != '-' else -1

        self.pawns = 0
        self.rooks = 0
        self.knights = 0
        self.bishops = 0
        self.queens = 0
        self.kings = 0

        self.white_pieces = 0
        self.black_pieces = 0

        self.white_can_castle_kingside = 'K' in castling
        self.white_can_castle_queenside = 'Q' in castling
        self.black_can_castle_kingside = 'k' in castling
        self.black_can_castle_queenside = 'q' in castling
        
        rank = 7
        file = 0

        for char in board_part:
            if char == '/':
                rank -= 1
                file = 0
                continue

            if char.isdigit():
                file += int(char)
                continue

            square = rank * 8 + file
            bit = 1 << square

            # Piece placement
            if char.lower() == 'p':
                self.pawns |= bit
            elif char.lower() == 'r':
                self.rooks |= bit
            elif char.lower() == 'n':
                self.knights |= bit
            elif char.lower() == 'b':
                self.bishops |= bit
            elif char.lower() == 'q':
                self.queens |= bit
            elif char.lower() == 'k':
                self.kings |= bit

            # Color
            if char.isupper():
                self.white_pieces |= bit
            else:
                self.black_pieces |= bit

            file += 1

    def print_board(self, tagged : list[int] = []):
        """
        Prints out a bitboard to stdout in a human-readable format.
        Uppercase pieces are white, lowercase are black.
        If tagged is set, colors all squares in tagged red.
        """
        piece_map = {}

        for i in range(64):
            mask = 1 << i
            if self.pawns & mask:
                piece_map[i] = "P"
            elif self.rooks & mask:
                piece_map[i] = "R"
            elif self.knights & mask:
                piece_map[i] = "N"
            elif self.bishops & mask:
                piece_map[i] = "B"
            elif self.queens & mask:
                piece_map[i] = "Q"
            elif self.kings & mask:
                piece_map[i] = "K"
            else:
                piece_map[i] = "."

            # Color
            if mask & self.black_pieces and piece_map[i] != ".":
                piece_map[i] = piece_map[i].lower()

        print("\n  a b c d e f g h")
        for rank in range(7, -1, -1):
            row = []
            for file in range(8):
                sq = rank * 8 + file
                if sq in tagged:
                    row.append('\033[91m' + piece_map[sq] + '\033[0m')
                else:
                    row.append(piece_map[sq])
            print(rank + 1, " ".join(row), rank + 1)
        print("  a b c d e f g h\n")

    def square_to_index(self, square):
        """
        Converts a square (for example, e2) to
        an index in the board
        """
        file = ord(square[0]) - ord('a')
        rank = int(square[1]) - 1
        return rank * 8 + file

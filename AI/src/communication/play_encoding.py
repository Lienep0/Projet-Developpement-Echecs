import chess
import numpy as np
import torch

class PlayEncoding():
    
    def encode(self, fen):
        board = chess.Board(fen)
        entry = self.update_entry(board)
        return torch.from_numpy(entry)


    def encode_pieces(self, board, entry, flip):
            piece_types = [
                chess.PAWN, chess.KNIGHT, chess.BISHOP,
                chess.ROOK, chess.QUEEN, chess.KING    
            ]

            for i, j in enumerate(piece_types):
                for square in board.pieces(j, chess.WHITE):
                    row, col = divmod(square, 8)
                    if flip: 
                        row = 7 - row
                        col = 7 - col
                    idx = i + 6 if flip else i
                    entry[idx, row, col] = 1.0
                    
                for square in board.pieces(j, chess.BLACK):
                    row, col = divmod(square, 8)
                    if flip: 
                        row = 7 - row
                        col = 7 - col
                    idx = i if flip else i + 6
                    entry[idx, row, col] = 1.0



    def fill_tactical_analysis(self, value, board, flip):
        for square in chess.SQUARES:
            row, col = divmod(square, 8)
            if flip: 
                row = 7-row
                col = 7-col
            if board.is_attacked_by(board.turn, square):
                value[21, row, col] = 1.0
            if board.is_attacked_by(not board.turn, square):
                value[22, row, col] = 1.0
                
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row, col = divmod(square, 8)
                if flip: 
                    row = 7-row
                    col = 7-col
                if board.is_pinned(piece.color, square):
                    value[23, row, col] = 1.0
                    
        return value

    def update_entry(self, board):
        value = np.zeros((24, 8, 8), dtype=np.float32)
        flip = True if board.turn == chess.BLACK else False
        self.encode_pieces(board, value, flip)
        value[12] = np.ones((8, 8))
        max_moves = 100.0
        current_move = board.fullmove_number
        normalized_value = min(current_move / max_moves, 1.0)
        value[13] = normalized_value
        if flip:
            value[14] = float(board.has_kingside_castling_rights(chess.BLACK))
            value[15] = float(board.has_queenside_castling_rights(chess.BLACK))
            value[16] = float(board.has_kingside_castling_rights(chess.WHITE))
            value[17] = float(board.has_queenside_castling_rights(chess.WHITE))
        else:
            value[14] = float(board.has_kingside_castling_rights(chess.WHITE))
            value[15] = float(board.has_queenside_castling_rights(chess.WHITE))
            value[16] = float(board.has_kingside_castling_rights(chess.BLACK))
            value[17] = float(board.has_queenside_castling_rights(chess.BLACK))
        if board.ep_square:
            row, col = divmod(board.ep_square, 8)
            if flip: 
                row = 7-row
                col = 7-col
            value[18, row, col] = 1.0
        value[19] = min(board.halfmove_clock / 100.0, 1.0)
        value[20] = 1.0 if board.is_check() else 0.0
        value = self.fill_tactical_analysis(value, board, flip)
        return value


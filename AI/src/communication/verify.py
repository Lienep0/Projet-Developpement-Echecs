import chess
import numpy as np
import torch

class Verify():
    def tensor_verify(self, fen):
        board = chess.Board(fen)
        mask = self.mask(board)
        return torch.from_numpy(mask)


    def mask(self,board):
        mask = np.zeros((73, 8, 8), dtype=np.float32)
        for move in board.legal_moves:
            plan, row, col = self.calculate_plan(move, board)
        
            if plan is not None:
                mask[plan, row, col] = 1.0
        return mask
    
    def calculate_plan(self, move, board):
        from_square = move.from_square
        to_square = move.to_square
        from_row, from_col = divmod(from_square, 8)
        to_row, to_col = divmod(to_square, 8)
        
        if board.turn == chess.BLACK:
            from_row, from_col = 7 - from_row, 7 - from_col
            to_row, to_col = 7 - to_row, 7 - to_col
            
        diff_row, diff_col = to_row - from_row, to_col - from_col
        distance = max(abs(diff_row), abs(diff_col))

        if move.promotion and move.promotion != chess.QUEEN:
            piece_type = {chess.KNIGHT: 0, chess.BISHOP: 1, chess.ROOK: 2}[move.promotion]
            direction = diff_col + 1 
            return 64 + (3 * piece_type) + direction, from_row, from_col

        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        if (diff_row, diff_col) in knight_moves:
            return 56 + knight_moves.index((diff_row, diff_col)), from_row, from_col
        
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for d_idx, (dr, dc) in enumerate(directions):
            if (diff_row == dr * distance) and (diff_col == dc * distance):
                return (d_idx * 7) + (distance - 1), from_row, from_col
                
        return None, None, None
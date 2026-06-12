import chess


#décodeur
class PlayDecoding():
    def __init__(self):
        self.index_to_move = {}
        self.move_to_index = {}
        
        empty_board = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1")
        for i in range(4672):
            move = self.get_tensor_move(i, empty_board)
            self.index_to_move[i] = move
            self.move_to_index[move] = i


    def get_tensor_move(self, move, board):
        flat_idx = move  
        plan_idx = flat_idx // 64
        remainder = flat_idx % 64
        r = remainder // 8
        c = remainder % 8  
        from_sq = r * 8 + c   
        to_sq = 0 
        p_type = None
        if plan_idx < 56:
            d_idx = plan_idx // 7
            dist = (plan_idx % 7) + 1
            dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            dr, dc = dirs[d_idx]
            to_sq = (r + dr * dist) * 8 + (c + dc * dist)
        elif plan_idx < 64:
            k_idx = plan_idx - 56
            knights = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
            dr, dc = knights[k_idx]
            to_sq = (r + dr) * 8 + (c + dc)
        else:
            p_idx = plan_idx - 64
            p_type = [chess.KNIGHT, chess.BISHOP, chess.ROOK][p_idx // 3]
            direction = (p_idx % 3) - 1
            dr = 1 
            to_sq = (r + dr) * 8 + (c + direction)
        move = chess.Move(from_sq, to_sq, promotion=p_type)
        if board.turn == chess.BLACK:
            from_sq_flipped = 63 - move.from_square
            to_sq_flipped = 63 - move.to_square
            move = chess.Move(from_sq_flipped, to_sq_flipped, promotion=move.promotion)     
        return move


    def get_move_tensor_id(self, move, board):
        if board.turn == chess.BLACK:
            f = 63 - move.from_square
            t = 63 - move.to_square
            move = chess.Move(f, t, promotion=move.promotion)
        
        return self.move_to_index.get(move, 0)
    

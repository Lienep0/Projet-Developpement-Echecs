import os
import h5py
import chess.pgn
import numpy as np


#nb parties : 60145

def update_value_head(game, board):
    value=np.zeros((3), dtype=np.float32)
    result = game.headers.get("Result")
    #victory
    if result == "1-0":
        value[2] = 1.0 
    #defeat
    elif result == "0-1":
        value[0] = 1.0   
    #draw
    else:
        value[1] = 1.0
    #current player
    if board.turn == chess.BLACK:
        value = value[::-1]
    return value 

def encode_pieces(board, entry):
    
    piece_types = [
        chess.PAWN, 
        chess.KNIGHT, 
        chess.BISHOP,
        chess.ROOK,  
        chess.QUEEN, 
        chess.KING    
    ]

    for i, j in enumerate(piece_types):
        for square in board.pieces(j, chess.WHITE):
            row, col = divmod(square, 8)
            entry[i, row, col] = 1.0

        for square in board.pieces(j, chess.BLACK):
            row, col = divmod(square, 8)
            entry[i + 6, row, col] = 1.0
    return entry



def fill_tactical_analysis(value, board):
    for square in chess.SQUARES:
        row, col = divmod(square, 8)
        if board.is_attacked_by(board.turn, square):
            value[21, row, col] = 1.0
        if board.is_attacked_by(not board.turn, square):
            value[22, row, col] = 1.0
            
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = divmod(square, 8)
            if board.is_pinned(piece.color, square):
                value[23, row, col] = 1.0
                
    return value

def update_entry(board):
    value = np.zeros((24, 8, 8), dtype=np.float32)
    encode_pieces(board,value)
    value[12] = np.ones((8, 8))
    max_moves = 100.0
    current_move = board.fullmove_number
    normalized_value = min(current_move / max_moves, 1.0)
    value[13] = normalized_value
    value[14] = float(board.has_kingside_castling_rights(chess.WHITE))
    value[15] = float(board.has_queenside_castling_rights(chess.WHITE))
    value[16] = float(board.has_kingside_castling_rights(chess.BLACK))
    value[17] = float(board.has_queenside_castling_rights(chess.BLACK))
    if board.ep_square:
        row, col = divmod(board.ep_square, 8)
        value[18, row, col] = 1.0
    value[19] = min(board.halfmove_clock / 100.0, 1.0)
    value[20] = 1.0 if board.is_check() else 0.0
    value = fill_tactical_analysis(value, board)
    return value

def update_policy_head(move, board):
    policy = np.zeros((73, 8, 8), dtype=np.float32)
    
    from_square = move.from_square
    to_square = move.to_square
    
    from_row, from_col = divmod(from_square, 8)
    to_row, to_col = divmod(to_square, 8)
    
    diff_row = to_row - from_row
    diff_col = to_col - from_col
    distance = max(abs(diff_row), abs(diff_col))
    if board.turn == chess.BLACK:
        from_row, from_col = 7 - from_row, from_col
        to_row, to_col = 7 - to_row, from_col
        diff_row = -diff_row

    if move.promotion and move.promotion != chess.QUEEN:
        direction = diff_col + 1 
        piece_type = {chess.KNIGHT: 0, chess.BISHOP: 1, chess.ROOK: 2}[move.promotion]
        plan_idx = 64 + (3 * piece_type) + direction
        policy[plan_idx, from_row, from_col] = 1.0
        return policy

    knight_moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    if (diff_row, diff_col) in knight_moves:
        plan_idx = 56 + knight_moves.index((diff_row, diff_col))
        policy[plan_idx, from_row, from_col] = 1.0
        return policy
    
    directions = [
        (1, 0), (1, 1), (0, 1), (-1, 1),
        (-1, 0), (-1, -1), (0, -1), (1, -1)
    ]
    
    for d_idx, (dr, dc) in enumerate(directions):
        if (diff_row == dr * distance) and (diff_col == dc * distance):
            plan_idx = (d_idx * 7) + (distance - 1)
            policy[plan_idx, from_row, from_col] = 1.0
            return policy

    return policy


def create_hdf5_file(h5_path):
    with h5py.File(h5_path, 'w') as f:
        f.create_dataset("entry", shape=(0, 24, 8, 8), maxshape=(None, 24, 8, 8), chunks=(1000, 24, 8, 8), dtype='f4')
        f.create_dataset("policy_head", shape=(0, 73, 8, 8), maxshape=(None, 73, 8, 8), chunks=(1000, 73, 8, 8), dtype='f4')
        f.create_dataset("value_head", shape=(0, 3), maxshape=(None, 3), chunks=(1000, 3), dtype='f4')


def write_encode(h5_file,PgnFile,index):
    buffer = 0
    while True:
        game = chess.pgn.read_game(PgnFile)
        if game is None:
            break 
        
        board = game.board() 

        entries = []
        policy_heads = []
        value_heads = []

        for move in game.mainline_moves():
            value_head = update_value_head(game,board)
            entry = update_entry(board)
            policy_head = update_policy_head(move, board)
            board.push(move)
            buffer+=1
            entries.append(entry)
            policy_heads.append(policy_head)
            value_heads.append(value_head)
            if buffer > 1000:
                index=save_position(h5_file, index,entries,policy_heads,value_heads,buffer)
                buffer = 0
                entries = []
                policy_heads = []
                value_heads = []
        if buffer > 0:
            index=save_position(h5_file, index,entries,policy_heads,value_heads,buffer)
            buffer = 0
            entries = []
            policy_heads = []
            value_heads = []
    pass
    return index


def save_position(h5_file, index, entries,policy_heads,value_heads,buffer):
    h5_file["entry"].resize(index+buffer, axis=0)
    h5_file["entry"][index:index+buffer] = np.array(entries)

    h5_file["policy_head"].resize(index+buffer, axis=0)
    h5_file["policy_head"][index:index+buffer] = np.array(policy_heads)

    h5_file["value_head"].resize(index+buffer, axis=0)
    h5_file["value_head"][index:index+buffer] = np.array(value_heads)

    index+=buffer

    return index







def iterate(h5_file,directory_path, limit):
    files = os.listdir(directory_path)
    index=0
    l=1
    for file in files:
        if file.endswith(".pgn"): 
            pgn = os.path.join(directory_path, file)
            with open(pgn, 'r') as f :
                index=write_encode(h5_file,f,index)
                if index>l*10000:
                    print(index)
                    l+=1
                if index>limit:
                    break
        else:
            continue

    
if __name__ == "__main__":
    limit = 1000000
    dirname = os.path.dirname(__file__)
    directory_path = os.path.join(dirname, 'PGN_files')

    h5_path = os.path.join(dirname, 'pretrain_moves_dataset.h5')

    if not os.path.exists(h5_path):
        create_hdf5_file(h5_path)

    with h5py.File(h5_path, 'a') as f:
        iterate(f,directory_path, limit)
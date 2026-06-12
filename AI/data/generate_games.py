import os
import h5py
import chess
import torch
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from encoding import TrainEncoding
from src.communication.play_encoding import PlayEncoding
from src.alphazero.inference_network import AI
from src.communication.verify import Verify
from src.communication.play_decoding import PlayDecoding
from src.communication.play_encoding import PlayEncoding
from src.communication.mcts import MCTSNode, RunMCTS



if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    AI_path = os.path.join(src_dir, 'final_model', 'AI_weights.pth')
    h5_path = os.path.join(dirname, 'self_play_moves_dataset.h5')
    train_encoder = TrainEncoding()

    if not os.path.exists(h5_path):
        train_encoder.create_hdf5_file(h5_path)
    start = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    board = chess.Board(start)
    encoder = PlayEncoding()
    decoder = PlayDecoding()
    model = AI().to(device)
    model.load_state_dict(torch.load(AI_path,map_location=device))
    model.eval()
    verify = Verify()

    iterations = 5

    with h5py.File(h5_path, 'a') as f:
        global_index = f['entry'].shape[0]

        for iteration in range(iterations):
            value_heads = []
            entries = []
            policy_heads = []
            board = chess.Board(start)
            root = MCTSNode(1.0, None, board.turn, board.fen(), model, encoder, decoder, verify, device,None)
            while not board.is_game_over():
                run_mcts = RunMCTS(root, 1)
                best_node = run_mcts.run()
            
                entries.append(encoder.encode(board.fen()).numpy())
                policy_heads.append(root.get_policy_vector().reshape(73, 8, 8))
                
                board.push(best_node.move)

                root = best_node
                root.parent = None
                        

            result = board.result()
            if result == "1-0":
                final_value=[1.0, 0.0, 0.0]
            elif result == "0-1":
                final_value=[0.0, 0.0, 1.0]
            else:
                final_value=[0.0, 1.0, 0.0]
            for _ in range(len(entries)):
                value_heads.append(final_value)
                final_value = final_value[::-1]
            
            global_index = train_encoder.save_position(f, global_index, entries, policy_heads, value_heads, len(entries))





import os
import sys
import chess
import torch
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from alphazero.inference_network import AI
from verify import Verify
from play_decoding import PlayDecoding
from play_encoding import PlayEncoding
from mcts import MCTSNode, RunMCTS


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    AI_path = os.path.join(root_dir, 'final_model', 'AI_weights.pth')
    fen = sys.argv[1]
    board = chess.Board(fen)
    encoder = PlayEncoding()
    decoder = PlayDecoding()
    verify = Verify()
    entry_tensor = encoder.encode(fen).unsqueeze(0).to(device)
    model = AI().to(device)
    model.load_state_dict(torch.load(AI_path,map_location=device))
    model.eval()
    root_mcts=MCTSNode(1.0,None,board.turn,fen,model,encoder,decoder,verify,device,None)
    best_node = RunMCTS(root_mcts,500).run()
    move_played = best_node.move
    uci = move_played.uci()
    print(uci)
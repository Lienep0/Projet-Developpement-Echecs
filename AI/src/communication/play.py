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
from training.mcts import MCTSNode, RunMCTS


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    dirname = os.path.dirname(__file__)
    AI_path = os.path.join(dirname, '..','..','final_model', 'AI_weights.pth')
    fen = sys.argv[1]
    board = chess.Board(fen)
    encoder = PlayEncoding()
    decoder = PlayDecoding()
    verify = Verify()
    entry_tensor = encoder.encode(fen).unsqueeze(0).to(device)
    model = AI().to(device)
    model.load_state_dict(torch.load(AI_path,map_location=device))
    model.eval()

    root_mcts=MCTSNode(1.0,None,board.turn,fen,model,encoder,decoder,verify,device)
    run = RunMCTS(root_mcts,500).run()
    final = run.state
    move_played = None
    for move in board.legal_moves:
        board.push(move)
        if board.fen() == final:
            move_played = move
            board.pop()
            break
        board.pop()
    uci = move_played.uci()
    print(uci)
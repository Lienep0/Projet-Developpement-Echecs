import os
import sys
import chess
import torch
sys.path.append("..")

from alphazero.inference_network import AI
from verify import Verify
from play_decoding import PlayDecoding
from play_encoding import PlayEncoding


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    dirname = os.path.dirname(__file__)
    AI_path = os.path.join(dirname, '..','..','final_model', 'AI_weights.pth')
    fen = sys.argv[1]
    board = chess.Board(fen)
    encoder = PlayEncoding()
    entry_tensor = encoder.encode(fen).unsqueeze(0).to(device)
    model = AI().to(device)
    model.load_state_dict(torch.load(AI_path,map_location=device))
    model.eval()

    with torch.no_grad():
        policy_tensor = model(entry_tensor)[0]
        policy_tensor = policy_tensor.squeeze(0)
    verify = Verify()
    mask = verify.tensor_verify(fen).to(device)

    policy_tensor = policy_tensor*mask
    decoder = PlayDecoding()
    uci = decoder.tensor_to_uci(policy_tensor.cpu(),board)
    print(uci)
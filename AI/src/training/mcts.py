import chess
import torch
import numpy as np


class RunMCTS:
    def __init__(self,root_mcts_node,iterations=100):
        self.root_mcts_node = root_mcts_node
        self.iterations = iterations
    def run(self):
        for i in range(self.iterations):
            node = self.root_mcts_node
            while node.children:
                node = node.best_child()
            if not node.visited:
                result = node.get_children()
            if not node.children:
                node.game_end = True
                if result == "1-0":
                    node.backpropagate(1.0)
                elif result == "0-1":
                    node.backpropagate(0.0) 
                else:
                    node.backpropagate(0.5)
            else:
                entry = node.encoder.encode(node.state).unsqueeze(0).to(node.device)
                with torch.no_grad():
                    val_preds = node.model(entry)[1][0]
                    value = (val_preds[0] * 1.0 + val_preds[1] * 0.0 + val_preds[2] * 0.5).item()
                node.backpropagate(value)
        choice = self.root_mcts_node.children[0]
        for child in self.root_mcts_node.children:
            if child.sum_visits>choice.sum_visits:
                choice = child
        return choice





class MCTSNode:
    def __init__(self, proba, parent, player, state,model,encoder,decoder,verify,device):
        self.state = state #plateau format fen
        self.parent = parent
        self.children = []
        self.player = player
        self.proba = proba
        self.sum_visits = 0
        self.sum_victory = 0
        self.game_end = False
        self.model = model #IA
        self.encoder = encoder
        self.decoder = decoder
        self.verify = verify
        self.visited = False
        self.device = device

    def puct(self):
        if not self.sum_visits:
            return float('inf')
        sum_visits_children = 0
        for child in self.parent.children:
            sum_visits_children += child.sum_visits
        puct = self.sum_victory/self.sum_visits + 2 * self.proba *  np.sqrt(sum_visits_children)/(1 + self.sum_visits)
        return puct

    def get_children(self):
        result = None
        board = chess.Board(self.state)
        end = board.is_game_over()
        if end :
            result = board.result()
            self.game_end = True
            return result
        if self.visited:
            return
        game_player = chess.BLACK if self.player == chess.WHITE else chess.WHITE
        entry_tensor = self.encoder.encode(self.state).unsqueeze(0).to(self.device)

        with torch.no_grad():
            policy_tensor = self.model(entry_tensor)[0]
            policy_tensor = policy_tensor.squeeze(0)
        mask = self.verify.tensor_verify(self.state).to(self.device)
        policy_tensor = (policy_tensor * mask).reshape(-1)
        indices = torch.nonzero(policy_tensor).reshape(-1)
        for i in range(indices.size(0)):
            move_id = indices[i].item()
            move = self.decoder.get_tensor_move(move_id, board)
            if move in board.legal_moves:
                prob = policy_tensor[move_id].item()
                new_board = board.copy()
                new_board.push(move)
                fen_move = new_board.fen()
                self.children.append(MCTSNode(prob, self, game_player, fen_move, self.model, self.encoder, self.decoder, self.verify, self.device))
        self.visited = True
        return result

        
    def best_child(self):
        choice = self.children[0]
        for child in self.children:
            if child.sum_visits == 0:
                return child
            elif child.puct()>choice.puct():
                choice = child
        return choice


    def backpropagate(self,value):
        self.sum_visits += 1
        self.sum_victory += value
        if self.parent:
            self.parent.backpropagate(1.0-value)
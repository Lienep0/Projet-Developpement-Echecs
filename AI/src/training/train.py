import os
import h5py
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from alphazero.train_network import AI

from torch import nn,optim
import torch
from torch.utils.data import TensorDataset, DataLoader

#entraîner le poids choisi dur les données choisies, ici le modèle de préentraînement sur les données du TCEC
def train(dataloaded,device,AI_path,epochs):
    model= AI().to(device)
    if os.path.exists(AI_path):
        model.load_state_dict(torch.load(AI_path,map_location=device))
    lossfn1 = nn.CrossEntropyLoss()
    lossfn2 = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    model.train()
    for epoch in range(epochs):
        total_loss1=0.0
        total_loss2=0.0
        for entry,policy_head,value_head in dataloaded:
            entry = entry.to(device)
            policy_head = policy_head.to(device)
            policy_head = policy_head.reshape(entry.size(0), 4672)
            value_head = value_head.to(device)
            optimizer.zero_grad()
            prediction_policy,prediction_value = model(entry)
            loss1 = lossfn1(prediction_policy, policy_head)
            loss2 = lossfn2(prediction_value, value_head)
            loss = loss1 + loss2
            total_loss1 += loss1.item()
            total_loss2 += loss2.item()
            loss.backward()
            optimizer.step()
        epoch_loss1 = total_loss1/len(dataloaded)
        epoch_loss2 = total_loss2/len(dataloaded)
        torch.save(model.state_dict(), AI_path)
        print(f'epoch numero : {epoch+1}, policy loss : {epoch_loss1}, value loss : {epoch_loss2} ')

if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    h5_path = os.path.join(dirname,'..','..','data','pretrain_moves_dataset.h5')
    AI_path = os.path.join(dirname, '..','..','pretrained_model', 'AI_weights.pth')
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

    with h5py.File(h5_path, "r") as f:
        entries = torch.from_numpy(f["entry"][:]).float()
        policy_heads = torch.from_numpy(f["policy_head"][:]).float()
        value_heads = torch.from_numpy(f["value_head"][:]).float()

    dataset = TensorDataset(entries,policy_heads,value_heads)
    dataloaded = DataLoader(dataset, batch_size=1024, shuffle=True)
    train(dataloaded,device,AI_path,10)

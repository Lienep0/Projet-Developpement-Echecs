import os
import h5py
from alphazero.network import IA


from torch import nn,optim
import torch
from torch.utils.data import TensorDataset, DataLoader


def train(dataloaded,device,AI_path,epochs):
    model= IA().to(device)
    lossfn1 = nn.CrossEntropyLoss()
    lossfn2 = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    model.train()
    for epoch in range(epochs):
        for entry,policy_head,value_head in dataloaded:
            entry = entry.to(device)
            policy_head = policy_head.to(device)
            value_head = value_head.to(device)
            optimizer.zero_grad()
            prediction_policy,prediction_value = model(entry)
            loss1 = lossfn1(prediction_policy, policy_head)
            loss2 = lossfn2(prediction_value, value_head)
            loss = loss1 + loss2
            loss.backward()
            optimizer.step()
        torch.save(model.state_dict(), AI_path)
        print(f'epoch numero :{epoch}')

if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    h5_path = os.path.join(dirname, '..', 'data/pretrain_moves_dataset.h5')
    AI_path = os.path.join(dirname, '..', 'src/AI_weights.pth')
    device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

    with h5py.File(h5_path, "r") as f:
        entries = torch.from_numpy(f["entry"][:]).float()
        policy_heads = torch.from_numpy(f["policy_head"][:]).float()
        value_heads = torch.from_numpy(f["value_head"][:]).float()

    dataset = TensorDataset(entries,policy_heads,value_heads)
    dataloaded = DataLoader(dataset, batch_size=512, shuffle=True)
    train(dataloaded,device,AI_path,1)

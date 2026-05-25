from torch import nn

epochs = 10000

class AI(nn.Module):
    def __init__(self, num=19):
        super().__init__()
        self.gelu = nn.GELU()
        self.conv = nn.Conv2d(24, 64, 3, stride=1, padding=1)
        self.batchnorm = nn.BatchNorm2d(64)

        self.resblocks = nn.ModuleList([ResBlock() for _ in range(num)])
        
        self.policy_head = OutBlockPolicyHead()
        self.value_head = OutBlockValueHead()
    
    def forward(self, x):
        x = self.conv(x)
        x = self.batchnorm(x)
        x = self.gelu(x)

        for resblock in self.resblocks :
            x = resblock(x)
        
        policy = self.policy_head(x)
        value = self.value_head(x)

        return policy, value
        
    
class ResBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.gelu = nn.GELU()
        self.conv1 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.batchnorm1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.batchnorm2 = nn.BatchNorm2d(64)
    
    def forward(self, x):
        xx = x
        x = self.gelu(self.batchnorm1(self.conv1(x)))
        x = self.batchnorm2(self.conv2(x))
        x = self.gelu(x + xx)
        return x


class OutBlockValueHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.gelu = nn.GELU()
        self.conv = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.batchnorm = nn.BatchNorm2d(64)
        self.linear = nn.Linear(4096, 3)
        """self.softmax = nn.Softmax(dim=1)"""

    def forward(self, x):
        x = self.conv(x)
        x = self.batchnorm(x)
        x = self.gelu(x)
        batch = x.size(0)
        x = x.reshape(batch,-1)
        x = self.linear(x)
        """x = self.softmax(x)"""
        """x = x.reshape(batch, 3)"""
        return x



class OutBlockPolicyHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.gelu = nn.GELU()
        self.conv = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.batchnorm = nn.BatchNorm2d(64)
        """self.softmax = nn.Softmax(dim=1)"""
        self.linear = nn.Linear(4096, 4672)

    def forward(self, x):
        x = self.conv(x)
        x = self.batchnorm(x)
        x = self.gelu(x)
        batch = x.size(0)
        x = x.reshape(batch,-1)
        x = self.linear(x)
        """x = self.softmax(x)"""
        """x = x.reshape(batch, 73,8,8)"""
        return x

















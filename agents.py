from environment import Uni
from torch import nn


class UniAI(nn.Module):
    def __init__(self, in_features, out_features):
        super(self, UniAI).__init__()
        self.fc = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLu(),
            nn.Linear(128, out_features)
        )

    def forward(self, x):
        return self.fc(x)


class Trader(Uni):
    def __init__(self, c1, c2, c3, c1_market, c2_market, c3_market):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c1_market = c1_market
        self.c2_market = c2_market
        self.c3_market = c3_market

    def model(self, in_features, out_features):
        self.model = UniAI(in_features, out_features)
        # place for a model

    def action(self):
        pass
    # action f(..) - > amount to trade in uniswap


class Arb(Uni):
    def __init__(self, c1, c2, c3):
        # define environment features
        pass

    def model(self):

    # define a model
    def action(self):
# action f(c1, c2, c3, hist,..) -> amount to sell
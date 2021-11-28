from environment import Uni
from torch import nn


def init_weights(m):
    if ((type(m) == nn.Linear)):
        nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.00)

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

#Basically arbitrageur will just swap his coins to sell them on market
class Arb(object):
    #uni1 - ETH/BTC current price with delta -> 0
    #uni2, uni2 - ETH/DAI, BTC/DAI
    def __init__(self, uni1, uni2, uni3, c1, c2, c3, h1, h2):
        self.init = (c1, c2, c3)
        self.init_market = (h1, h2)
        self.uni1 = uni1
        self.uni2 = uni2
        self.uni3 = uni3
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.h1 = h1
        self.h2 = h2
        self.model = UniAI(8, 5)
        for param in self.model.parameters():
            param.requires_grad = False
        init_weights(self.model)


    def get_action(self, vector):
        real_action = self.model(vector)

        if real_action[0] > 0:
            real_action[0] = min(real_action[0], self.c1)
            self.c1 -= real_action[0]
        else:
            real_action[0] = max(-self.c2, real_action[0])
            self.c2 += real_action[0]

        if real_action[1] > 0:
            real_action[1] = min(real_action[1], self.c1)
            self.c1 -= real_action[1]
        else:
            real_action[1] = max(-self.c3, real_action[1])
            self.c3 += real_action[1]

        if real_action[2] > 0:
            real_action[2] = min(real_action[2], self.c2)
            self.c2 -= real_action[2]
        else:
            real_action[2] = max(-self.c3, real_action[2])
            self.c3 += real_action[2]
        self.real_action = real_action

        return real_action
        #output[:3] will be the amounts of coins to swap on the Uni1, Uni2, Uni3 pools
        #sign is important here: if vector[0] > 0 agent will swap ETH for BTC, else if vector[0] <= 0 agent will swap BTC for ETH
        #the same is for ETH/DAI and BTC/DAI
    #eth/btc, eth/dai, btc/dai

    def upd_portfolio(self, deltas, h1, h2):
        self.h1 = h1
        self.h2 = h2  # update market prices
        if self.real_action[0] > 0:
            self.c2 += deltas[0]
        else:
            self.c1 += deltas
        if self.real_action[1] > 0:
            self.c3 += deltas[2]
        else:
            self.c1 += deltas[1]
        if self.real_action[2] > 0:
            self.c3 += deltas[2]
        else:
            self.c2 += deltas[2]

    #eth/dai, btc/dai
    def sell(self):
        if self.real_action[3] > 0:
            self.real_action[3] = min(self.c1, self.real_action[3])
            self.c1 -= self.real_action[3]
            self.c3 += self.real_action[3] * self.h1
        else:
            self.real_action[3] = max(self.real_action[3], -self.c3)
            self.c1 -= self.real_action[3]
            self.c3 += self.real_action[3] * self.h1

        if self.real_action[4] > 0:
            self.real_action[4] = min(self.c2, self.real_action[4])
            self.c2 -= self.real_action[4]
            self.c3 += self.real_action[4] * self.h2
        else:
            self.real_action[4] = max(self.real_action[4], -self.c3)
            self.c2 -= self.real_action[4]
            self.c3 += self.real_action[4] * self.h2

    def get_return(self):
        return (self.c1 * self.h1  + self.c2 * self.h2 + self.c3) / (self.init[0] * self.init_market[0] + self.init[1] * self.init_market[1] + self.init[2])


#trader only sees uniswap and is not interested in selling coins to markets
class Trader(object):
    def __init__(self, uni1, uni2, uni3, c1, c2, c3, h1, h2):
        self.init_market = (h1, h2)
        self.init = (c1, c2, c3)
        self.uni1 = uni1
        self.uni2 = uni2
        self.uni3 = uni3
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.model = UniAI(6, 3)
    #eth/btc, eth/dai, btc/dai
    # define a model
    def get_action(self, vector):
        real_action = self.model(vector)

        if real_action[0] > 0:
            real_action[0] = min(real_action[0], self.c1)
            self.c1 -= real_action[0]
        else:
            real_action[0] = max(-self.c2, real_action[0])
            self.c2 += real_action[0]

        if real_action[1] > 0:
            real_action[1] = min(real_action[1], self.c1)
            self.c1 -= real_action[1]
        else:
            real_action[1] = max(-self.c3, real_action[1])
            self.c3 += real_action[1]

        if real_action[2] > 0:
            real_action[2] = min(real_action[2], self.c2)
            self.c2 -= real_action[2]
        else:
            real_action[2] = max(-self.c3, real_action[2])
            self.c3 += real_action[2]
        self.real_action = real_action

    def upd_portfolio(self, deltas, h1, h2):
        self.h1 = h1
        self.h2 = h2  # updating market prices
        if self.real_action[0] > 0:
            self.c2 += deltas[0]
        else:
            self.c1 += deltas
        if self.real_action[1] > 0:
            self.c3 += deltas[2]
        else:
            self.c1 += deltas[1]
        if self.real_action[2] > 0:
            self.c3 += deltas[2]
        else:
            self.c2 += deltas[2]

    def get_return(self):
        return (self.c1 * self.h1  + self.c2 * self.h2 + self.c3) / (self.init[0] * self.init_market[0] + self.init[1] * self.init_market[1] + self.init[2])



# action f(c1, c2, c3, hist,..) -> amount to sell
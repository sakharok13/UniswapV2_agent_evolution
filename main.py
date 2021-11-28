from evolution import *
from agents import *
from environment import *
import pandas as pd

def main():
    t = 0
    btc_hist = pd.read_csv('BTC-USD.csv')['Open']
    eth_hist = pd.read_csv('ETH-USD.csv')['Open']
    assert(len(eth_hist) == len(btc_hist)), 'history lengths should be equal'

    dai_hist = np.random.normal(loc = 1, scale = 0.01, size=len(eth_hist))
    e2b = Uni(np.random.rand() * 50, np.random.rand() * 10, eth_hist, btc_hist)
    e2d = Uni(np.random.rand() * 20, np.random.rand() * 1000, eth_hist, dai_hist)
    b2d = Uni(np.random.rand() * 20, np.random.rand() * 15000, eth_hist, dai_hist)


    #define agents on these environments
    #let them evolve

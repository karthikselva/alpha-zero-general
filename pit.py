import Arena
from MCTS import MCTS
from minichess.GardnerMiniChessGame import GardnerMiniChessGame, display
from minichess.BabyChessGame import BabyChessGame
from minichess.MalletChessGame import MalletChessGame
from minichess.MiniChessPlayer import *
from minichess.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = GardnerMiniChessGame(5)

# all players
rp1 = RandomPlayer(g).play
rp2 = RandomPlayer(g).play
gp1 = GreedyPlayer(g).play

# nnet players
n21 = NNet(g)
n21.load_checkpoint('./pretrained_models/minichess/keras/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 200, 'cpuct':1.0})
mcts1 = MCTS(g, n21, args1)
n21p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
verbose = False
print('')
print(' Neural Network (v21) vs Random Player')
print('----------------------------------------')
arena = Arena.Arena(n21p, rp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

print('')
print(' Neural Network (v21) vs Greedy Player')
print('----------------------------------------')

arena = Arena.Arena(n21p, gp1, g, display=display)
print(arena.playGames(20, verbose=verbose))


args1 = dotdict({'numMCTSSims': 200, 'cpuct':1.0})
mcts1 = MCTS(g, n15, args1)
n15p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
print('')
print(' Neural Network (v21) vs Neural Network (v15)')
print('----------------------------------------')

arena = Arena.Arena(n21p, n15p, g, display=display)
print(arena.playGames(20, verbose=verbose))
n15 = NNet(g)
n15.load_checkpoint('./pretrained_models/minichess/keras/','checkpoint_15.pth.tar')

# all players
rp1 = RandomPlayer(g).play
gp1 = GreedyPlayer(g).play

print('')
print(' Neural Network (v15) vs Random Player')
print('----------------------------------------')

arena = Arena.Arena(n15p, rp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

print('')
print(' Neural Network (v15) vs Greedy Player')
print('----------------------------------------')

arena = Arena.Arena(n15p, gp1, g, display=display)
print(arena.playGames(20, verbose=verbose))


n10 = NNet(g)
n10.load_checkpoint('./pretrained_models/minichess/keras/','checkpoint_10.pth.tar')
args1 = dotdict({'numMCTSSims': 200, 'cpuct':1.0})
mcts1 = MCTS(g, n10, args1)
n10p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
print('')
print(' Neural Network (v21) vs Neural Network (v10)')
print('----------------------------------------')

arena = Arena.Arena(n21p, n10p, g, display=display)
print(arena.playGames(20, verbose=verbose))
# all players
rp1 = RandomPlayer(g).play
gp1 = GreedyPlayer(g).play

print('')
print(' Neural Network (v10) vs Random Player')
print('----------------------------------------')

arena = Arena.Arena(n10p, rp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

print('')
print(' Neural Network (v10) vs Greedy Player')
print('----------------------------------------')

arena = Arena.Arena(n10p, gp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

n6 = NNet(g)
n6.load_checkpoint('./pretrained_models/minichess/keras/','checkpoint_6.pth.tar')
args1 = dotdict({'numMCTSSims': 200, 'cpuct':1.0})
mcts1 = MCTS(g, n6, args1)
n6p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
print('')
print(' Neural Network (v21) vs Neural Network (v6)')
print('----------------------------------------')

arena = Arena.Arena(n21p, n6p, g, display=display)
print(arena.playGames(20, verbose=verbose))
# all players
rp1 = RandomPlayer(g).play
gp1 = GreedyPlayer(g).play

print('')
print(' Neural Network (v6) vs Random Player')
print('----------------------------------------')

arena = Arena.Arena(n6p, rp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

print('')
print(' Neural Network (v6) vs Greedy Player')
print('----------------------------------------')

arena = Arena.Arena(n6p, gp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

g = BabyChessGame(5)

# all players
rp1 = RandomPlayer(g).play
rp2 = RandomPlayer(g).play
gp1 = GreedyPlayer(g).play

# nnet players
n21 = NNet(g)
n21.load_checkpoint('./pretrained_models/minichess/keras/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 200, 'cpuct':1.0})
mcts1 = MCTS(g, n21, args1)
n21p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

print('')
print('Baby Chess -  Neural Network (v21) vs Random Player')
print('----------------------------------------')
arena = Arena.Arena(n21p, rp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

print('')
print('Baby Chess -  Neural Network (v21) vs Greedy Player')
print('----------------------------------------')

arena = Arena.Arena(n21p, gp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

g = MalletChessGame(5)

# all players
rp1 = RandomPlayer(g).play
rp2 = RandomPlayer(g).play
gp1 = GreedyPlayer(g).play

# nnet players
n21 = NNet(g)
n21.load_checkpoint('./pretrained_models/minichess/keras/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 200, 'cpuct':1.0})
mcts1 = MCTS(g, n21, args1)
n21p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

print('')
print('Mallet Chess -  Neural Network (v21) vs Random Player')
print('----------------------------------------')
arena = Arena.Arena(n21p, rp1, g, display=display)
print(arena.playGames(20, verbose=verbose))

print('')
print('Mallet Chess -  Neural Network (v21) vs Greedy Player')
print('----------------------------------------')

arena = Arena.Arena(n21p, gp1, g, display=display)
print(arena.playGames(20, verbose=verbose))
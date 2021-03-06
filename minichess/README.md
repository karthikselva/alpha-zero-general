# Scaling Up Alpha Zero General (Minichess)

An implementation of a simple game provided to check extendability of the framework. Main difference of this game comparing to Othello is that it allows draws, i.e. the cases when nobody won after the game ended. To support such outcomes ```Arena.py```, ``MCTS.py``` and ```Coach.py``` classes were modified.

To train a model for MiniChess, change the imports in ```main.py``` to:

```python
from Coach import Coach
from minichess.MiniChessGame import Game
from minichess.keras.NNet import NNetWrapper as nn
from utils import *
```

 Make similar changes to ```pit.py```.

To start training a model for Minichess:
```bash
python main.py
```
To start a tournament of 10 episodes with the model-based player against a random player:
```bash
python pit.py
```
You can check the results of RandomPlayer vs Neural Network Player in ```pit.py```

### Experiments
I trained a Keras model for 5X5 Minichess (10 iterations, 25 episodes, 10 epochs per iteration and 25 MCTS simulations per turn). This took about 15 minutes on an i7-7330 with CUDA Nvida GTX 960. The pretrained model (Keras) can be found in ```pretrained_models/minichess/keras/```.

## Implementation Details

1. Initializing and displaying the Minichess Board
2. Checking whether game has ended or not
3. Defining players Player 1 and Player 2
4. Checking valid moves and mapping moves to Grid Points (to be enhanced to a3g5 format later)
5. Play all pieces one by one and validate (Pawn, Rook, King, Queen, Knight and Bishop)
6. Check Pawn cross attack
7. Check Pawn to reach last move and become Queuen
8. Complete the Game and check the winner



## Section 1 - Initializing and displaying the Minichess Board


- Load inital libraries


```python
from Coach import Coach
from minichess.GardnerMiniChessGame import GardnerMiniChessGame as Game
from minichess.MiniChessLogic import Board
from minichess.keras.NNet import NNetWrapper as nn
from utils import *
import numpy as np
```



- Load the Game and required Neural Network


```python
g = Game()
nnet = nn(g)
board = g.getInitBoard()
n = 5 # 5X5 Grid
logic = Board(n,board)
print(np.array(board))
```

    [[  -479   -280   -320   -929 -60000]
     [  -100   -100   -100   -100   -100]
     [     0      0      0      0      0]
     [   100    100    100    100    100]
     [   479    280    320    929  60000]]


## Section 2 - Checking whether game has ended or not

- Verify the Canonical and User Board


```python
player1 = 1
player2 = -1
g.display(board,player1)
```


    ♜ ♞ ♝ ♛ ♚
    ♟ ♟ ♟ ♟ ♟
    ·  ·  ·  ·  ·
    ♙ ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔


- Check whether Game is ended
- It should return 0 since Game is still in Valid state


```python
print(g.getGameEnded(board,player1))
```

    0


## Section 4 - Checking valid moves and mapping moves to Grid Points (to be enhanced to a3g5 format later)

- Check the next legal move we can do
- It Should list all Pawn moves for White and Horse moves

[(36, 29), (37, 30), (38, 31), (39, 32), (40, 33), (44, 29), (44, 31)]



Overal Chess Grid 5X5 Looks like this:

        # Chess GRID with Padding and Cell Number
        # [0,  1,  2,  3,  4,  5,  6]
        # [7,  8,  9,  10, 11, 12, 13]

        # [14,   15, 16, 17, 18, 19,     20]
        # [21,   22, 23, 24, 25, 26,     27]
        # [28,   29, 30, 31, 32, 33,     34]
        # [35,   36, 37, 38, 39, 40,     41]
        # [42,   43, 44, 45, 46, 47,     48]

        # [49, 50, 51, 52, 53, 54, 55]
        # [56, 57, 58, 59, 60, 61, 62]



```python
print('\nAll possible moves are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
g.display(board,player2)
```


    All possible moves are:

    [(100, 36, 29), (100, 37, 30), (100, 38, 31), (100, 39, 32), (100, 40, 33), (280, 44, 29), (280, 44, 31)]

    ♜ ♞ ♝ ♛ ♚
    ♟ ♟ ♟ ♟ ♟
    ·  ·  ·  ·  ·
    ♙ ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔


- Execute first move by moving the White Pawn from a2 to a3

move = (36,29)


```python
logic.execute_move((1,36,29),player1)
g.display(logic.pieces_without_padding(),player1)
```


    ♖ ♘ ♗ ♕ ♔
    ·  ♙ ♙ ♙ ♙
    ♙ ·  ·  ·  ·
    ♟ ♟ ♟ ♟ ♟
    ♜ ♞ ♝ ♛ ♚


- Assign Player 2 as -1
- Get Legal moves for Player 2
- Execute one pawn Move


```python
player2 = -1
print('\nAll possible moves are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
g.display(logic.pieces_without_padding(),player1)
```


    All possible moves are:

    [(100, 37, 30), (100, 37, 29), (100, 38, 31), (100, 39, 32), (100, 40, 33), (280, 44, 29), (280, 44, 31)]

    ♖ ♘ ♗ ♕ ♔
    ·  ♙ ♙ ♙ ♙
    ♙ ·  ·  ·  ·
    ♟ ♟ ♟ ♟ ♟
    ♜ ♞ ♝ ♛ ♚


## Section 4 - Checking valid moves and mapping moves to Grid Points (to be enhanced to a3g5 format later)

Overal Chess Grid 5X5 Looks like this:

        # Chess GRID with Padding and Cell Number
        # [0,  1,  2,  3,  4,  5,  6]
        # [7,  8,  9,  10, 11, 12, 13]

        # [14,   15, 16, 17, 18, 19,     20]
        # [21,   22, 23, 24, 25, 26,     27]
        # [28,   29, 30, 31, 32, 33,     34]
        # [35,   36, 37, 38, 39, 40,     41]
        # [42,   43, 44, 45, 46, 47,     48]

        # [49, 50, 51, 52, 53, 54, 55]
        # [56, 57, 58, 59, 60, 61, 62]

Now make a horse move from b1 to a3


```python
logic.execute_move((1,44,29),player2)
g.display(logic.pieces_without_padding(),player1)
```


    ♜ ·  ♝ ♛ ♚
    ♟ ♟ ♟ ♟ ♟
    ♞ ·  ·  ·  ·
    ·  ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔


- White to take the horse
- List legal moves and take the horse


```python
print('\nAll possible moves are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
g.display(logic.pieces_without_padding(),player1)
```


    All possible moves are:

    [(100, 37, 30), (100, 37, 29), (100, 38, 31), (100, 39, 32), (100, 40, 33), (479, 43, 36), (479, 43, 29), (280, 44, 29), (280, 44, 31)]

    ♜ ·  ♝ ♛ ♚
    ♟ ♟ ♟ ♟ ♟
    ♞ ·  ·  ·  ·
    ·  ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔



```python
logic.execute_move((1,44,29),player1)
g.display(logic.pieces_without_padding(),player1)
print('\nAll possible moves are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
```


    ♖ ·  ♗ ♕ ♔
    ·  ♙ ♙ ♙ ♙
    ♘ ·  ·  ·  ·
    ♟ ♟ ♟ ♟ ♟
    ♜ ·  ♝ ♛ ♚

    All possible moves are:

    [(100, 37, 30), (100, 37, 29), (100, 38, 31), (100, 39, 32), (100, 40, 33), (479, 43, 44)]


## Section 5 - Play all pieces one by one and validate (Pawn, Rook, King, Queen, Knight and Bishop)

Refer the Grid to Make a move


Overal Chess Grid 5X5 Looks like this:

        # Chess GRID with Padding and Cell Number
        # [0,  1,  2,  3,  4,  5,  6]
        # [7,  8,  9,  10, 11, 12, 13]

        # [14,   15, 16, 17, 18, 19,     20]
        # [21,   22, 23, 24, 25, 26,     27]
        # [28,   29, 30, 31, 32, 33,     34]
        # [35,   36, 37, 38, 39, 40,     41]
        # [42,   43, 44, 45, 46, 47,     48]

        # [49, 50, 51, 52, 53, 54, 55]
        # [56, 57, 58, 59, 60, 61, 62]




```python
logic.execute_move((1,37,29),player2)
g.display(logic.pieces_without_padding(),player1)
print('\nAll possible moves are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
```


    ♜ ·  ♝ ♛ ♚
    ♟ ·  ♟ ♟ ♟
    ♟ ·  ·  ·  ·
    ·  ♙ ♙ ♙ ♙
    ♖ ·  ♗ ♕ ♔

    All possible moves are:

    [(100, 37, 30), (100, 37, 23), (100, 37, 29), (100, 38, 31), (100, 39, 32), (100, 40, 33), (479, 43, 36), (479, 43, 29), (479, 43, 44)]



```python
logic.execute_move((1,43,29),player1)
g.display(logic.pieces_without_padding(),player1)
print('\nAll possible moves are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
```


    ·  ·  ♗ ♕ ♔
    ·  ♙ ♙ ♙ ♙
    ♖ ·  ·  ·  ·
    ♟ ·  ♟ ♟ ♟
    ♜ ·  ♝ ♛ ♚

    All possible moves are:

    [(100, 38, 31), (100, 39, 32), (100, 40, 33), (479, 43, 44), (320, 45, 37), (320, 45, 29)]



```python
logic.execute_move((1,45,29),player2)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 1 are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
```


    ♜ ·  ·  ♛ ♚
    ♟ ·  ♟ ♟ ♟
    ♝ ·  ·  ·  ·
    ·  ♙ ♙ ♙ ♙
    ·  ·  ♗ ♕ ♔

    All possible moves for Player 1 are:

    [(100, 37, 30), (100, 37, 23), (100, 37, 29), (100, 38, 31), (100, 39, 32), (100, 40, 33)]



```python
logic.execute_move((1,37,29),player1)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 2 are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
```


    ·  ·  ♗ ♕ ♔
    ·  ·  ♙ ♙ ♙
    ♙ ·  ·  ·  ·
    ♟ ·  ♟ ♟ ♟
    ♜ ·  ·  ♛ ♚

    All possible moves for Player 2 are:

    [(100, 38, 31), (100, 39, 32), (100, 40, 33), (479, 43, 44), (479, 43, 45), (929, 46, 45), (929, 46, 44)]



```python
logic.execute_move((1,46,44),player2)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 1 are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
```


    ♜ ♛ ·  ·  ♚
    ♟ ·  ♟ ♟ ♟
    ♙ ·  ·  ·  ·
    ·  ·  ♙ ♙ ♙
    ·  ·  ♗ ♕ ♔

    All possible moves for Player 1 are:

    [(100, 38, 31), (100, 39, 32), (100, 40, 33), (320, 45, 37)]



```python
logic.execute_move((1,39,32),player1)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 2 are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
```


    ·  ·  ♗ ♕ ♔
    ·  ·  ♙ ·  ♙
    ♙ ·  ·  ♙ ·
    ♟ ·  ♟ ♟ ♟
    ♜ ♛ ·  ·  ♚

    All possible moves for Player 2 are:

    [(100, 38, 31), (100, 38, 32), (100, 40, 33), (100, 40, 32), (929, 44, 37), (929, 44, 30), (929, 44, 23), (929, 44, 16), (929, 44, 45), (929, 44, 46), (60000, 47, 46)]



```python
logic.execute_move((1,44,37),player2)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 1 are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
```


    ♜ ·  ·  ·  ♚
    ♟ ♛ ♟ ♟ ♟
    ♙ ·  ·  ♙ ·
    ·  ·  ♙ ·  ♙
    ·  ·  ♗ ♕ ♔

    All possible moves for Player 1 are:

    [(100, 29, 23), (100, 32, 24), (100, 32, 26), (100, 38, 31), (100, 40, 33), (320, 45, 37), (320, 45, 39), (320, 45, 33), (929, 46, 39), (60000, 47, 39)]


## Section 7 -  Check Pawn to reach last move and become Queuen



```python
logic.execute_move((1,32,24),player1)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 2 are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
```


    ·  ·  ♗ ♕ ♔
    ·  ·  ♙ ·  ♙
    ♙ ·  ·  ·  ·
    ♟ ♛ ♙ ♟ ♟
    ♜ ·  ·  ·  ♚

    All possible moves for Player 2 are:

    [(929, 37, 45), (929, 37, 29), (929, 37, 31), (929, 37, 25), (929, 37, 19), (929, 37, 30), (929, 37, 23), (929, 37, 16), (929, 37, 38), (929, 37, 44), (100, 39, 32), (100, 39, 25), (100, 40, 33), (479, 43, 44), (479, 43, 45), (479, 43, 46), (60000, 47, 46)]



```python
logic.execute_move((1,37,25),player2)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 1 are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)
```


    ♜ ·  ·  ·  ♚
    ♟ ·  ♙ ♟ ♟
    ♙ ·  ·  ·  ·
    ·  ·  ♙ ♛ ♙
    ·  ·  ♗ ♕ ♔

    All possible moves for Player 1 are:

    [(100, 24, 17), (100, 38, 31), (100, 40, 33), (320, 45, 37), (320, 45, 39), (929, 46, 39), (60000, 47, 39)]



```python
logic.execute_move((1,24,17),player1)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 2 are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
```


    ·  ·  ♗ ♕ ♔
    ·  ·  ♙ ♛ ♙
    ♙ ·  ·  ·  ·
    ♟ ·  ·  ♟ ♟
    ♜ ·  ♕ ·  ♚

    All possible moves for Player 2 are:

    [(929, 25, 33), (929, 25, 31), (929, 25, 37), (929, 25, 17), (929, 25, 19), (929, 25, 18), (929, 25, 26), (929, 25, 32), (929, 25, 24), (100, 39, 32), (100, 40, 33), (479, 43, 44), (479, 43, 45), (60000, 47, 46)]


## Section 8 - Complete the Game and check the winner



```python
logic.execute_move((1,25,19),player2)
g.display(logic.pieces_without_padding(),player1)

print('\nAll possible moves for Player 1 are: \n')
moves = []
for move in logic.get_legal_moves(player1):
    moves.append(move)
print(moves)

```


    ♜ ·  ♕ ·  ♚
    ♟ ·  ·  ♟ ♟
    ♙ ·  ·  ·  ·
    ·  ·  ♙ ·  ♙
    ·  ·  ♗ ♕ ♛

    All possible moves for Player 1 are:

    [(929, 17, 25), (929, 17, 23), (929, 17, 18), (929, 17, 19), (929, 17, 24), (929, 17, 31), (929, 17, 16), (929, 17, 15), (100, 38, 31), (100, 38, 24), (100, 40, 33), (320, 45, 37), (320, 45, 39), (320, 45, 33), (929, 46, 39), (929, 46, 32), (929, 46, 25), (929, 46, 47)]



```python
print(logic.is_win(player2))
print(logic.is_win(player1))
print(g.getGameEnded(logic.pieces_without_padding(),player2))
```

    True
    False
    1


## Section 9 - Normalize Actions to Ids

- Every piece can take any position in 5 X 5 Grid
- Queen Can move diagonally and straig from every cell (0,0), (0,1) .... (3,1) ... (4,4)
- Similarly every piece can move to all possible positions constrained by their rule
- We will store two hash maps
- Action Identifier to Actions   { 51: ["Queen", "Cell 1", "Cell 10"], ... }
- Action to Action Identifier    { "Queen:Cell1:Cell10": 242, ... }


```python
print(g.id_to_action[100])
print(g.action_to_id["479:31:38"])
```

    (479, 31, 38)
    100


- Action size really huge compared to other board games because of different piece type and moves
- This grows exponentially high once the board size starts growing (say n = 8)


```python
print(len(g.id_to_action))
```

    942


## Section 10 - Get All Valid Moves in the MCTS consumable format

Overal Chess Grid 5X5 Looks like this:

        # Chess GRID with Padding and Cell Number
        # [0,  1,  2,  3,  4,  5,  6]
        # [7,  8,  9,  10, 11, 12, 13]

        # [14,   15, 16, 17, 18, 19,     20]
        # [21,   22, 23, 24, 25, 26,     27]
        # [28,   29, 30, 31, 32, 33,     34]
        # [35,   36, 37, 38, 39, 40,     41]
        # [42,   43, 44, 45, 46, 47,     48]

        # [49, 50, 51, 52, 53, 54, 55]
        # [56, 57, 58, 59, 60, 61, 62]



```python
import numpy as np
g = Game()
nnet = nn(g)
board = g.getInitBoard()
n = 5 # 5X5 Grid
logic = Board(n,board)
print(np.array(board))
print('\nAll possible moves for Player 2 are: \n')
moves = []
for move in logic.get_legal_moves(player2):
    moves.append(move)
print(moves)
print(len(g.action_to_id))
valids = g.getValidMoves(board,player1)
print(len(valids))
count = 0
for i in valids:
    if i == 1: count += 1
print(count)
print(len(moves))

```

    [[  -479   -280   -320   -929 -60000]
     [  -100   -100   -100   -100   -100]
     [     0      0      0      0      0]
     [   100    100    100    100    100]
     [   479    280    320    929  60000]]

    All possible moves for Player 2 are:

    [(100, 36, 29), (100, 37, 30), (100, 38, 31), (100, 39, 32), (100, 40, 33), (280, 44, 29), (280, 44, 31)]
    942
    942
    7
    7


## Section 11 - Train with MCTS

- Changed Neural Network activation from softmax to sigmoid due to vanishing gradients
- Never use numpy array and python array mixed
- Rotation and player switching in canonical board might be conufusing


```python
from Coach import Coach
from minichess.GardnerMiniChessGame import GardnerMiniChessGame as Game
from minichess.keras.NNet import NNetWrapper as nn
from utils import *

args = dotdict({
    'numIters': 10,
    'numEps': 5,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200,
    'arenaCompare': 10,
    'numMCTSSims': 25,
    'cpuct': 1,
    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

g = Game()
nnet = nn(g)
c = Coach(g, nnet, args)

```


```python
c.executeEpisode()
c.executeEpisode()
c.executeEpisode()
print()
```


    ·  ♜ ♝ ·  ♚
    ·  ♟ ·  ·  ♟
    ·  ♟ ♗ ♙ ♙
    ·  ♖ ♞ ·  ·
    ·  ♛ ♕ ·  ♔
    Player -1 won

    ♜ ♞ ·  ·  ♚
    ♟ ·  ♘ ♟ ·
    ♝ ·  ·  ♙ ·
    ♙ ♙ ♟ ·  ♛
    ♖ ·  ♗ ·  ♔
    Player -1 won

    ·  ·  ·  ♛ ♚
    ♜ ·  ·  ·  ·
    ♝ ·  ♕ ♟ ♟
    ♙ ·  ·  ♙ ♙
    ♖ ♘ ♛ ·  ♔
    Player -1 won



### Contributors and Credits
* [Karthik selvakumar Bhuvaneswaran](https://github.com/karthikselva)

The implementation is based on the game of Othello (https://github.com/suragnair/alpha-zero-general/tree/master/othello).

### AlphaGo / AlphaZero Events
* February 8, 2018 - [Solving Alpha Go Zero + TensorFlow, Kubernetes-based Serverless AI Models on GPU](https://www.meetup.com/Advanced-Spark-and-TensorFlow-Meetup/events/245308722/)

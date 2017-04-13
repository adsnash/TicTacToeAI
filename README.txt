I did some research on how to best implement a Tic Tac Toe AI, and all signs pointed to the Minimax Algorithm (there are a number of blogs/websites that discuss how it works in much more detail, Google "tic tac toe minimax" and you should have no trouble finding one). It recursively calls every possible board state to determine the best move. A winning move for the player is 10 points, a win for the opponent is -10 points, and a draw is 0 points. 

At every other level of depth, it switches off between the player and opponent and tries to pick the optimal score. This means that the player will try to maximize the score while the opponent will try to minimize it. By switching back and forth, it prevents the AI from picking a move that will allow the opponent to win (unless there are no other options). 

There is an additional layer of complexity that records the depth of the tree and subtracts it from the score. This means that the algorithm will favor moves that lead to a faster victory and will still attempt to win even if a cat’s game seems imminent. 

Ultimately, the algorithm will select the move that leads to the highest possible score. I have played the AI a number of times and have yet to beat it. I don’t expect to either. I haven’t tried EVERY possible combination of moves, but I feel that would be a moot point. For all intents and purposes, this AI is unbeatable. 

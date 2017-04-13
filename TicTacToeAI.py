#! python3

import sys

class Board():

    def __init__(self):
        self.theBoard = []

    '''reset board to initial starting state'''
    def resetBoard(self):
        self.theBoard = []
        for i in range(9):
            self.theBoard.append(' ')

    '''used with printBoard, either show space number or player mark'''
    def boardSpot(self, num):
        if self.theBoard[num] == ' ':
           return str(num+1)
        else:
            return self.theBoard[num]

    '''print the current board state'''
    def printBoard(self):
        print(self.boardSpot(6)+'|'+self.boardSpot(7)+'|'+self.boardSpot(8))
        print('-+-+-')
        print(self.boardSpot(3)+'|'+self.boardSpot(4)+'|'+self.boardSpot(5))
        print('-+-+-')
        print(self.boardSpot(0)+'|'+self.boardSpot(1)+'|'+self.boardSpot(2))

    '''check for win - generic so AI can use , must pass board as argument'''
    def checkWin(self, board, player):
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] == player:
                return True
        for i in range(0,9,3):
            if board[i] == board[i+1] == board[i+2] == player:
                return True
        if board[0] == board[4] == board[8] == player:
                return True
        elif board[2] == board[4] == board[6] == player:
                return True
        else:
            return False
    
class Player:

    def __init__(self):
        self.marker = None

    '''set player mark, can be changed if rematch is called'''
    def setMarker(self, marker):
        self.marker = marker

    '''Get input from user, check that move is valid'''
    def playerTurn(self):
        spot = None
        while True:
            try:
                spot = int(input('Select a spot to move (1 - 9): ')) -1
            except ValueError:
                print('You think you\'re so clever, don\'t you?')
            if 0 <= spot <= 8 and GameBoard.theBoard[spot] == ' ':
                GameBoard.theBoard[spot] = self.marker
                break
            else:
                print('Invalid move. Please pick a non-taken number 1 through 9')
                GameBoard.printBoard()

class AI:

    def __init__(self):
        self.marker = None
        self.enemy = None

    '''set player marks, can be changed if rematch is called'''
    def setMarkers(self, marker, enemy):
        self.marker = marker
        self.enemy = enemy

    '''given board state, check for a winner/cat's game and return a score'''
    def complete(self, board, depth):
        if GameBoard.checkWin(board, self.marker):
            return 10 - depth
        elif GameBoard.checkWin(board, self.enemy):
            return -10 + depth
        else:
            for i in range(9):
                if board[i] == ' ':
                    return None
            return 0
            
    '''given board state, get all possible moves'''
    def getOptions(self, board):
        options = []
        for i in range(9):
            if board[i] == ' ':
                options.append(i)
        if options == []:
            return None
        else:
            return options

    '''Minimax Algorithm to determine best possible move for a given board by
    recursively creating every possible move. See README.txt for more details.
    '''
    def minimax(self, board, player, enemy, depth=0):
        '''if move set reaches an endgame state, return corresponding score'''
        score = self.complete(board, depth)
        if score != None:
            return score
        elif score == None:
            '''otherwise get available moves'''
            options = self.getOptions(board)
            if options == None:
                return 0
            scoreList = []
            depth += 1
            for i in options:
                newBoard = list(board)
                newBoard[i] = player
                '''Recursively call minimax to get a score for every move, but 
                switch which marker is player and enemy to optimize for next
                level of depth. If move does not lead to an endgame state,
                minimax will continue going deeper until an endgame is reached.
                '''
                value = self.minimax(newBoard, enemy, player, depth)
                '''append value directly if score returned, or append score from
                lower level's optimization. 
                '''
                if type(value) is int:
                    scoreList.append((value, i))
                else:
                    scoreList.append((value[0], i))
            '''maximize or minimize score depending on which player would move
            on corresponding level of depth. Return score and depth as tuple so
            both score and move are retained. This allows for higher depths to
            just use the score and for the final result to get the board space.
            '''
            if player == self.marker:
                m = max(scoreList)
                return m
            else:
                m = min(scoreList)
                return m

    '''calls minimax to get the best option and makes its move'''
    def makeMove(self):
        board = list(GameBoard.theBoard)
        spot = self.minimax(board, self.marker, self.enemy)
        GameBoard.theBoard[spot[1]] = self.marker

class GameControl:

    def __init__(self):
        self.restart = True
        self.playerTurn = None

    '''allow the player to decide who goes first'''
    def startUp(self):
        self.playerTurn = None
        while True:
            choice = input('Do you want to be X or O: ')
            if choice.lower() == 'x':
                self.playerTurn = True
            elif choice.lower() == 'o':
                self.playerTurn = False
            if self.playerTurn != None:
                break
            else:
                print('Come on now, this is the easy part!\n')

    '''game loop to control the flow of the game and switch back and forth'''
    def gameLoop(self):
        print('Let\'s do this.\n')
        self.restart = False
        GameBoard.resetBoard()
        for i in range(9):
            GameBoard.printBoard()
            if self.playerTurn:
                self.playerTurn = False
                print('\nYour Turn')
                Human.playerTurn()
                if GameBoard.checkWin(GameBoard.theBoard, Human.marker):
                    print('You won!? It must have been a fluke!')
                    break
            else:
                self.playerTurn = True
                print('\nMy Turn')
                Computer.makeMove()
                if GameBoard.checkWin(GameBoard.theBoard, Computer.marker):
                    print('I win! No surprises there.')
                    break
            if i == 8:
                print('Cat\'s game. Lucky break, I\'ll beat you next time!\n')
        GameBoard.printBoard()

    '''on game loop completion, handle for rematch or quitting'''
    def rematch(self):
        press = input('Press q to quit or any other key for a rematch: ')
        if press.lower() == 'q':
            print('\nSo long, space cowboy!')
            sys.exit()
        else:
            self.restart = True

'''instantiate Board, Player, and AI objects to manipulate with gameControl'''
GameBoard = Board()
Human = Player()
Computer = AI()

def main():
    print('Hello, human. Let\'s see if you can beat me at Tic Tac Toe.')
    Game = GameControl()
    while Game.restart:
        Game.startUp()
        if Game.playerTurn:
            Human.setMarker('X')
            Computer.setMarkers('O','X')
        else:
            Human.setMarker('O')
            Computer.setMarkers('X','O')
        Game.gameLoop()
        Game.rematch()

if __name__ == '__main__':
    main()

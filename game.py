import board
import sys
import numpy as np


class Position:
    counter = 0

    def __init__(self, myBoard, players, level = 0, move = None):
        self.myBoard = myBoard
        #print(myBoard.board)
        self.players = players
        self.myPlayer = players.nextPlayer()
        self.myMove = move
        self.children = []
        self.level = level
        self.loser = None
        print(self.level*'  ', move, 'by: ', self.myPlayer.symbol)
        if self.myMove == None:
            self.analyse()

    def checkILost(self):
        res =  self.myBoard.checkSquareEfficient(self.myMove)
        if res:
            print(
                'Losing move ',self.myMove,' by ',self.myPlayer.symbol)
            print(self.myBoard.board)
            #displaySquare(self.myBoard.size, res)
            #sys.exit(0)
            self.loser = self.myPlayer.symbol
            return True

        return False

    def getOpponentSymbol(self):
        if self.myPlayer.symbol == 1:
            return 0
        else:
            return 1

    def analyse(self):
        if self.myMove != None:
            self.myBoard.addToken(
                self.myMove[0], self.myMove[1], self.myPlayer.symbol)
            res = self.checkILost()
            if res:
                self.myBoard.addToken(
                    self.myMove[0], self.myMove[1], 0)
                return(self)

        self.legalMoves = self.myBoard.getEmpty()
        #print(self.level*'  ', "testing: ", self.legalMoves)
        if len(self.legalMoves) == 0:
            print(self.myBoard.board)
            print("Draw")
            self.loser = None
            self.myBoard.board[self.myMove[0], self.myMove[1]] = 0
            Position.counter = Position.counter + 1
            if Position.counter == 10:
                sys.exit(0)
            return self

        self.players.advancePlayer()

        for move in self.legalMoves:
            self.children.append(
                Position(self.myBoard, self.players, self.level + 1, move))
            self.children[-1].analyse()

        #print(self.level, self.myMove, self.myPlayer.symbol)
        #print([(x.loser, x.myMove) for x in self.children])

        myres = self.getOpponentSymbol()
        for x in self.children:
            if x.loser == self.myPlayer.symbol:
                myres = self.myPlayer.symbol
                break
            elif x.loser == None:
                myres = None
        self.loser = myres


        if self.myMove != None:
            self.myBoard.addToken(self.myMove[0], self.myMove[1], 0)
            self.players.advancePlayer() #really going back
            print("\n", self.myBoard.board)
            return(self)
        else:
            print("Analysis ended")
    
def displaySquare(n, corners):
    res = np.zeros((n,n),dtype=int)
    for c in corners:
        res[c[0], c[1]] = 1

    print(res)



if __name__ == '__main__':
    player1 = board.Player(1)
    player2 = board.Player(2)
    players = board.PlayerList([player1, player2])
    print(players.nextPlayer().symbol)
    board = board.Board(3, players)
    pos = Position(board, players)
    #pos.analyse()
    print(pos.loser)

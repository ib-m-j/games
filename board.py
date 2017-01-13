import numpy as np
import random
import sys

random.seed()


class Player:
    def __init__(self, symbol, name = ''):
        self.symbol = symbol
        if name == '':
            name = symbol
        self.name = name


class PlayerList:
    def __init__(self, listOfPlayers):
        self.players = listOfPlayers
        self.nextPlayerNo = 0

    def advancePlayer(self):
        if self.nextPlayerNo == len(self.players) - 1:
            self.nextPlayerNo = 0
        else:
            self.nextPlayerNo = self.nextPlayerNo + 1
        return self.players[self.nextPlayerNo]
    
    def nextPlayer(self):
        return self.players[self.nextPlayerNo]

class Board:
    def __init__(self, n, players):
        self.board = np.zeros((n,n), dtype=int)
        self.players = players
        self.size = n
        self.subSquares = self.findSubSquares()
        self.makeSquareLookup()


    def addToken(self, a, b, token):
        assert(0<=a and a<self.size)
        assert(0<=b and b<self.size)
        self.board[a][b] = token

    def fillTokens(self, player):
        for i in range(self.size):
            for j in range(self.size):
                self.addToken(i, j, player.symbol)

    def findSubSquares(self):
        self.squares = []
        for i in range(self.size):
            for j in range(self.size):
                start = np.array([i,j])
                for da in range(1, self.size - i):
                    for db in range(self.size - j):
                        res = isSquare(self.size,start,np.array([da,db]))
                        if res:
                            self.squares.append(res)
        return self.squares
    
    def squareLookupKey(self, position):
        return position[0]*self.size + position[1]
        
        
    def makeSquareLookup(self):
        self.squareLookup = {}
        for i in range(self.size*self.size):
            self.squareLookup[i] = []
        for s in self.squares:
            for c in s:
                self.squareLookup[self.squareLookupKey(c)].append(s)


    def getEmpty(self):
        res = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i,j] == 0:
                    res.append(np.array([i,j]))
        return res

    def checkSquareEfficient(self, selected):
        symbol = self.players.nextPlayer().symbol
        for s in self.squareLookup[self.squareLookupKey(selected)]:
            #displaySquare(self.size, s)
            found = True
            for c in s:
                cFound = s
                if self.board[c[0], c[1]] != symbol:
                    found = False
                    break
            if found:
                break
        if found: 
            return cFound
        
        return None
            

    def fillRandom(self):
        while True:
            possible = self.getEmpty()
            if len(possible) == 0:
                break
        
            selected = possible[random.randrange(len(possible))]
            self.board[
                selected[0], selected[1]] = self.players.nextPlayer().symbol
            #foundSquare = self.checkSquare(
            #    selected, self.players.nextPlayer().symbol)
            foundSquare = self.checkSquareEfficient(selected)
            if foundSquare != None:
                print('****')
                print(self.board)
                print("selected", selected)
                displaySquare(self.size, foundSquare)
                print("found square", self.players.nextPlayer().symbol)

            self.players.advancePlayer()
        
        
    def checkSquare(self, selected, symbol):
        symbol = self.board[selected[0], selected[1]]
        for s in self.subSquares:
                res = None
                for c in s:
                    res = s 
                    if self.board[c[0],c[1]] != symbol:
                        res = None
                        break
                    
                if res != None:
                    found = False
                    for c in s:
                        if c[0] == selected[0] and c[1] == selected[1]:
                            found = True
                    if found:
                        return res
                    else:
                        return None
                    
        return None


def isSquare(n,start,sidea):
    sideb = np.array([sidea[1], -sidea[0]])
    e = start + sideb
    f = e + sidea
    if (0<=e[1] and e[0] < n and
        f[0] < n and f[1] < n):
        return ([start, start+sidea, e, f])
    else:
        return None

def displaySquare(n, corners):
    res = np.zeros((n,n),dtype=int)
    for c in corners:
        res[c[0], c[1]] = 1

    print(res)

def displaySquares(n, squares):
    res = np.zeros((n,n),dtype=int)
    for s in squares:
        for c in s:
            res[c[0], c[1]] = res[c[0], c[1]] + 1

    print(res)
    
def squareTest():
    
    player1 = Player('a')
    player2 = Player('b')
    board = Board(4, PlayerList([player1, player2]))

    allSquares = board.findSubSquares()
    for x in allSquares:
        print(x)
        displaySquare(4, x)

    displaySquares(4,  allSquares)                      
    
    
def boardTest():
    player1 = Player(1)
    player2 = Player(2)
    board = Board(4, PlayerList([player1, player2]))
    board.fillRandom()


if __name__ == '__main__':
    #player1 = Player(1)
    #player2 = Player(2)
    #board = Board(2, PlayerList([player1, player2]))
    #board.fillTokens(player1)
    #res = board.checkSquareEfficient([0,0])
    #print(res)
    boardTest()
    print("\nstarting b\n")

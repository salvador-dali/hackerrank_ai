from random import choice
import os

def printMatrix(matrix):
    for i in xrange(10):
        print matrix[i]
    print

#TODO add multiplier 0.8 for ships that are connected to each other
class battleship:
    def parseInput(self, board):
        # based on the input, creates the internal state, which allow to make everything faster
        # have not tried, missed, hit, killed
        dictionary = {'m': 0, 'd': 1, 'h': 5, '-': 8}
        state = 'searching'
        for i in xrange(10):
            for j in xrange(10):
                # if we only hit the ship, we need to hunt it
                # also all H elements should be saved and later the probability should be 0 for them
                if board[i][j] == 'h':
                    state = 'hunting'
                    self.elementsShouldBeZero.append([i, j])

                self.board[i][j] = dictionary[board[i][j]]

        self.state = state

    def tryInsertShip(self, shipLength, numOfShips):
        # try to insert a ship of a particular length to each position
        # if the ship can be inserted, then the score matrix will be updated with the numberOfShips
        for i in xrange(10):
            for j in xrange(10):
                # if there is at least one Miss or Dead there, then the ship is not able to fit there

                if self.state == 'searching':
                    # try horizontal ship
                    if j < 11 - shipLength and 2 < min(self.board[i][j:j + shipLength]):
                        for z in xrange(j, j + shipLength):
                            self.score[i][z] += numOfShips

                    # no need to do this twice if this is 1x1 ship
                    if shipLength > 1:
                        # try vertical ship
                        if i < 11 - shipLength and 2 < min([self.board[l][j] for l in xrange(i, i + shipLength)]):
                            for z in xrange(i, i + shipLength):
                                self.score[z][j] += numOfShips

                # we can not hunt a 1x1 ship. It can not be just hit, it should be dead or missed
                elif self.state == 'hunting' and shipLength > 1:
                    # try horizontal ship
                    if j < 11 - shipLength:
                        newList = self.board[i][j:j + shipLength]
                        if 2 < min(newList) and (5 in newList):
                            for z in xrange(j, j + shipLength):
                                # if on this row we have many hits -it is more likely
                                self.score[i][z] += numOfShips * newList.count(5)

                    # try vertical ship
                    if i < 11 - shipLength:
                        newList = [self.board[l][j] for l in xrange(i, i + shipLength)]
                        if 2 < min(newList) and (5 in newList):
                            for z in xrange(i, i + shipLength):
                                # if on this column we have many hits -it is more likely
                                self.score[z][j] += numOfShips * newList.count(5)

    def calculateProbability(self):
        # inserts the ship of each type
        for i in self.ships:
            if self.ships[i]:
                self.tryInsertShip(i, self.ships[i])

        # change all elements to 0 for places where it was a H
        for i in self.elementsShouldBeZero:
            self.score[i[0]][i[1]] = 0

    def findShoutingTarget(self):
        # based on the probability matrix from self.score, selects the best possible target
        # search type = 1 means that you are searching from all the elements based on their probability
        # type = 0 only randomly select the biggest randomly Based on testing, performs worse
        # if searchType:
        #     elemDictionary = {}
        #     for i in xrange(10):
        #         for j in xrange(10):
        #             tmp = self.score[i][j]
        #             if tmp > 0:
        #                 elemDictionary[str(i) + '_' + str(j)] = tmp
        #
        #     return map(int, choice([b for b in elemDictionary for a in range(elemDictionary[b])]).split('_'))
        maximumValue, positions = 0, []
        for i in xrange(10):
            for j in xrange(10):
                tmp = self.score[i][j]
                if tmp > maximumValue:
                    maximumValue = tmp
                    positions = [(i, j)]
                elif tmp == maximumValue:
                    positions.append((i, j))

        return choice(positions)

    def saveState(self, y, x):
        # have to save information about number of ships and the current shot
        # saves the number of survived ships
        # [1, 2, 3, 4, 5]
        # this information looks like this
        #
        # 1 2 0 0 1
        # 3 2
        # this means that 1 1x1 ship has survived, 2 1x2 ships and 1 1x5
        # also the current shot was in 3, 2
        ships = [self.ships[i] for i in xrange(1, 6)]

        stringBoard = ''
        for i in self.board:
            stringBoard += ''.join(map(str, i)) + '\n'

        with open('battleship.txt', "w") as f:
            f.write(' '.join(map(str, ships)) + '\n' + str(y) + ' ' + str(x) + '\n' + stringBoard)

    def updateShipInfo(self):
        difference = []
        for i in xrange(10):
            for j in xrange(10):
                a, b = self.board[i][j], self.prevBoard[i][j]
                if a != b and (a != 0 or b != 8):
                    difference.append([i, j, a, b])

        print 'Board difference : ' + str(difference)
        print 'Game state : ' + self.state

        if self.lastShot and self.board[self.lastShot[0]][self.lastShot[1]] == 1:
            # you killed the ship
            s = 1
            for i in difference:
                if i[3] == 5:
                    s += 1

            print 'Killed a 1x' + str(s) + ' ship'
            if self.ships[s] > 0:
                self.ships[s] -= 1

        print 'Survived ships : ' + str(self.ships)
        print

    def getState(self):
        # parses the information from the state file and sets inner information of a class
        filename = "battleship.txt"
        if os.path.isfile(filename):
            with open(filename) as f:
                lines = f.readlines()
                ships, lastShot = map(int, lines[0].strip().split(' ')), list(map(int, lines[1].strip().split(' ')))

                prevBoard = [map(int, list(i.strip())) for i in lines[2:]]
                self.prevBoard = prevBoard
        else:
            ships, lastShot = [2, 2, 1, 1, 1], None
            self.prevBoard = [[8 for col in xrange(10)] for row in xrange(10)]

        self.lastShot = lastShot
        self.ships = {i + 1: ships[i] for i in xrange(5)}

    def __init__(self, board):
        # private state of the game
        # information about the board, probabilistic score
        # lastShot (in the previous state)
        # how many ships survived so far
        # and are we Searching or Hunting
        self.board = [[0 for col in xrange(10)] for row in xrange(10)]
        self.prevBoard = None
        self.score = [[0 for col in xrange(10)] for row in xrange(10)]
        self.lastShot = None
        self.ships = None
        self.state = None
        self.elementsShouldBeZero = []

        self.getState()
        print 'Previous shot  : ' + str(self.lastShot)
        print 'Survived ships : ' + str(self.ships)
        print 'Previous board  : (0 - missed, 1 - killed, 8 - have not tried, 5 - hit)'
        printMatrix(self.prevBoard)
        self.parseInput(board)
        print 'Current board  : (0 - missed, 1 - killed, 8 - have not tried, 5 - hit)'
        printMatrix(self.board)
        self.updateShipInfo()
        self.calculateProbability()
        print 'Current probability : '
        printMatrix(self.score)

arr = [
    #0123456789
    '----------', #0
    '----d--m--', #1
    '--m---m---', #2
    '-m------m-', #3
    '---ddddd--', #4
    '-m---m--m-', #5
    '--m-d--mdd', #6
    '---md-m-m-', #7
    '---md--m--', #8
    '----d-----'  #9
]
game = battleship(arr)
y, x = game.findShoutingTarget()
print 'Current shot : ' + str(y) + ' ' + str(x)
game.saveState(y, x)

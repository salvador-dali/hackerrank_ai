# board representation. First player plays vertically, second horizontally
from random import randint, seed, choice

TOTAL = 8
def numToBoard(num, n=TOTAL):
    arr = [int(i) for i in bin(num)[2:].zfill(n*n)]
    return [arr[n*i:n*i+n] for i in xrange(n)]

def boardToNum(board):
    return int(''.join([str(item) for line in board for item in line]), 2)

def isFirstTurn(board):
    return sum(item for line in board for item in line) / 2 % 2 == 0

# helpers

def isTerminal(node, n=TOTAL):
    """"
    When the first player moves, check whether there is at least one vertical two-space
    available at his disposal. If it is, than the node is not terminal.
    Similar idea is for the horizontal player
    """
    board = numToBoard(node)
    if isFirstTurn(board):
        return not any(board[i][j] + board[i + 1][j] == 0 for j in xrange(n) for i in xrange(n - 1))
    else:
        return not any(board[i][j] + board[i][j + 1] == 0 for j in xrange(n - 1) for i in xrange(n))

def getChildren(node, n=TOTAL):
    board = numToBoard(node)
    if isFirstTurn(board):
        for i in xrange(n - 1):
            for j in xrange(n):
                if board[i][j] + board[i + 1][j] == 0:
                    board[i][j], board[i + 1][j] = 1, 1
                    yield boardToNum(board)
                    board[i][j], board[i + 1][j] = 0, 0
    else:
        for i in xrange(n):
            for j in xrange(n - 1):
                if board[i][j] + board[i][j + 1] == 0:
                    board[i][j], board[i][j + 1] = 1, 1
                    yield boardToNum(board)
                    board[i][j], board[i][j + 1] = 0, 0

def getHeuristicValue(node):
    return randint(-5, 5)

def alpha_beta_negamax_with_move(node, depth, a, b, color):
    if depth == 0 or isTerminal(node):
        return color * getHeuristicValue(node), None

    bestValue, bestMoves = float('-inf'), []
    for child in getChildren(node):
        val, _ = alpha_beta_negamax_with_move(child, depth - 1, -b, -a, -color)
        m_val = - val
        if m_val > bestValue:
            bestValue, bestMoves = m_val, [child]
        elif m_val == bestValue:
            bestMoves.append(child)

        a = max(a, m_val)
        if a >= b:
            break
    return bestValue, choice(bestMoves)

def printBoard(node):
    board = numToBoard(node)
    for line in board:
        print ''.join(['x' if i else '.' for i in line])
    print

def play():
    node, moveNum = 0, 1
    while True:
        board = numToBoard(node)
        color = 1 if isFirstTurn(board) else -1
        _, node = alpha_beta_negamax_with_move(node, 1, float('-inf'), float('inf'), color)
        if node is None:
            # print '=========='
            # if moveNum % 2:
            #     print 'Second won'
            # else:
            #     print 'First won'
            # print '=========='
            return moveNum % 2

        # print 'Move number', moveNum
        # printBoard(node)
        moveNum += 1


print sum(play() for i in xrange(10000))

"""
board representation. First player plays vertically, second horizontally
5x5 is the win for black
"""
from random import randint, choice, seed
from datetime import datetime

seed(0)
n = 8
def numToBoard(node):
    arr = [int(i) for i in bin(node)[2:].zfill(n*n)]
    return [arr[n*i:n*i+n] for i in xrange(n)]

def boardToNum(board):
    return int(''.join([str(item) for line in board for item in line]), 2)

def isFirstTurn(board):
    return sum(item for line in board for item in line) / 2 % 2 == 0

def isTerminal(node):
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

def getChildrenVertical(board):
    children = []
    for i in xrange(n - 1):
        for j in xrange(n):
            if board[i][j] + board[i + 1][j] == 0:
                board[i][j], board[i + 1][j] = 1, 1
                children.append(boardToNum(board))
                board[i][j], board[i + 1][j] = 0, 0
    return children

def getChildrenHorizontal(board):
    children = []
    for i in xrange(n):
        for j in xrange(n - 1):
            if board[i][j] + board[i][j + 1] == 0:
                board[i][j], board[i][j + 1] = 1, 1
                children.append(boardToNum(board))
                board[i][j], board[i][j + 1] = 0, 0
    return children

def getChildren(node):
    board = numToBoard(node)
    if isFirstTurn(board):
        return getChildrenVertical(board)

    return getChildrenHorizontal(board)


def alpha_beta(node, depth, a, b, color, f):
    if depth == 0 or isTerminal(node):
        return color * f(node), None

    bestValue, bestMoves = float('-inf'), []
    for child in getChildren(node):
        val, _ = alpha_beta(child, depth - 1, -b, -a, -color, f)
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

# --------- Evaluation functions
def getValueRandom(node):
    return randint(0, 5)

def getValueFirst(node):
    board = numToBoard(node)
    player_1 = sum(board[i][j] + board[i + 1][j] == 0 for j in xrange(n) for i in xrange(n - 1))
    player_2 = sum(board[i][j] + board[i][j + 1] == 0 for j in xrange(n - 1) for i in xrange(n))
    return player_1 - player_2

def getValueSecond(node):
    board = numToBoard(node)
    first = isFirstTurn(board)
    player_1 = sum(board[i][j] + board[i + 1][j] == 0 for j in xrange(n) for i in xrange(n - 1))
    player_2 = sum(board[i][j] + board[i][j + 1] == 0 for j in xrange(n - 1) for i in xrange(n))

    total = float(player_1 + player_2)
    value = -1 if first else 1
    if total == 0:
        return value

    return (player_1 - player_2 + value / 25.0) / total

# -------------
def playOneGame(f1, f2):
    node, num = 0, 1
    while node is not None:
        board = numToBoard(node)
        color = 1 if isFirstTurn(board) else -1
        if color == 1:
            # first player
            _, node = alpha_beta(node, 4, float('-inf'), float('inf'), color, f1)
        else:
            # second player
            _, node = alpha_beta(node, 4, float('-inf'), float('inf'), color, f2)

        if node:
            getValueFirst(node)
            num += 1
            # print getValueSecond(node), getValueFirst(node)
            # printBoard(node)


    # has first won
    # print 'Is first won', num % 2 == 0
    return num % 2 == 0

def competition(first, second, rounds):
    res = sum(playOneGame(first, second) for _ in xrange(rounds))
    print 'Out of ' + str(rounds) + ' rounds as white, Player1 won ' + str(res)
    res = sum(playOneGame(second, first) for _ in xrange(rounds))
    print 'Out of ' + str(rounds) + ' rounds as black, Player1 won ' + str(rounds - res)

pass
# print alpha_beta(17788, 4, float('-inf'), float('inf'), 1, getValueSecond)
# startTime = datetime.now()
# competition(getValueFirst, getValueSecond, 500)
# print datetime.now() - startTime

# num, n = 4932659095546419968, 8

def isSafeVertical(board, i, j):
    if j == 0:
        if board[i][j + 1] == 1 and board[i + 1][j + 1] == 1:
            return True
    elif j == n - 1:
        if board[i][j - 1] == 1 and board[i + 1][j - 1] == 1:
            return True
    elif board[i][j + 1] == 1 and board[i + 1][j + 1] == 1 and board[i][j - 1] == 1 and board[i + 1][j - 1] == 1:
        return True

    return False

def extractSafeVertical(num):
    board_modify, board_copy, moves = numToBoard(num), numToBoard(num), []
    for i in xrange(n - 1):
        for j in xrange(n):
            if board_modify[i][j] == 0 and board_modify[i + 1][j] == 0 and isSafeVertical(board_modify, i, j):
                board_modify[i][j], board_modify[i + 1][j] = 1, 1
                board_copy[i][j], board_copy[i + 1][j] = 1, 1
                moves.append(boardToNum(board_copy))
                board_copy[i][j], board_copy[i + 1][j] = 0, 0

    return moves

def isSafeHorizontal(board, i, j):
    if i == 0:
        if board[i + 1][j] == 1 and board[i + 1][j + 1] == 1:
            return True
    elif i == n - 1:
        if board[i - 1][j] == 1 and board[i - 1][j + 1] == 1:
            return True
    elif board[i + 1][j] == 1 and board[i + 1][j + 1] == 1 and board[i - 1][j] == 1 and board[i - 1][j + 1] == 1:
        return True
    return False

def extractSafeHorizontal(num):
    board_modify, board_copy, moves = numToBoard(num), numToBoard(num), []
    for i in xrange(n):
        for j in xrange(n - 1):
            if board_modify[i][j] == 0 and board_modify[i][j + 1] == 0 and isSafeHorizontal(board_modify, i, j):
                board_modify[i][j], board_modify[i][j + 1] = 1, 1
                board_copy[i][j], board_copy[i][j + 1] = 1, 1
                moves.append(boardToNum(board_copy))
                board_copy[i][j], board_copy[i][j + 1] = 0, 0

    return moves

def isStrategicalVertical(board, i, j):
    moves = []

    board[i][j], board[i + 1][j] = 1, 1
    if isSafeVertical(board, i, j + 1):
        moves.append(boardToNum(board))
    board[i][j], board[i + 1][j] = 0, 0

    board[i][j + 1], board[i + 1][j + 1] = 1, 1
    if isSafeVertical(board, i, j):
        moves.append(boardToNum(board))
    board[i][j + 1], board[i + 1][j + 1] = 0, 0

    return moves

def extractStrategicalVertical(num):
    board_modify, board_copy, moves, total = numToBoard(num), numToBoard(num), [], 0
    for i in xrange(n - 1):
        for j in xrange(n - 1):
            if board_modify[i][j] == 0 and board_modify[i][j + 1] == 0 and board_modify[i + 1][j] == 0 and board_modify[i + 1][j + 1] == 0:
                tmp_moves = isStrategicalVertical(board_copy, i, j)
                if tmp_moves:
                    board_modify[i][j], board_modify[i][j + 1], board_modify[i + 1][j], board_modify[i + 1][j + 1] = 1, 1, 1, 1
                    total += 1
                    moves += tmp_moves

    return total, moves

def isStrategicalHorizontal(board, i, j):
    moves = []
    board[i][j], board[i][j + 1] = 1, 1
    if isSafeHorizontal(board, i + 1, j):
        moves.append(boardToNum(board))
    board[i][j], board[i][j + 1] = 0, 0

    board[i + 1][j], board[i + 1][j + 1] = 1, 1
    if isSafeHorizontal(board, i, j):
        moves.append(boardToNum(board))
    board[i + 1][j], board[i + 1][j + 1] = 0, 0

    return moves

def extractStrategicalHorizontal(num):
    board_modify, board_copy, moves, total = numToBoard(num), numToBoard(num), [], 0
    for i in xrange(n - 1):
        for j in xrange(n - 1):
            if board_modify[i][j] == 0 and board_modify[i][j + 1] == 0 and board_modify[i + 1][j] == 0 and board_modify[i + 1][j + 1] == 0:
                tmp_moves = isStrategicalHorizontal(board_copy, i, j)
                if tmp_moves:
                    board_modify[i][j], board_modify[i][j + 1], board_modify[i + 1][j], board_modify[i + 1][j + 1] = 1, 1, 1, 1
                    total += 1
                    moves += tmp_moves

    return total, moves

def getChildren_2(node):
    if isFirstTurn(numToBoard(node)):
        safe_moves = extractSafeVertical(node)
        _, strategical_moves = extractStrategicalVertical(node)
    else:
        safe_moves = extractSafeHorizontal(node)
        _, strategical_moves = extractStrategicalHorizontal(node)

    irrelevant = set(strategical_moves + safe_moves)

    all_children = list(getChildren(node))
    print 'All moves', len(all_children)
    print 'Safe moves', len(safe_moves)
    print 'Strategical moves', len(strategical_moves)

    for i in strategical_moves:
        printBoard(i)

    left_moves = [i for i in getChildren(node) if i not in irrelevant]
    print len(left_moves)

    sorted_moves = strategical_moves + left_moves
    if len(sorted_moves):
        return sorted_moves

    return safe_moves


def getValueThird(node):
    board = numToBoard(node)
    first = isFirstTurn(board)

    all_1, all_2 = getChildrenVertical(board), getChildrenHorizontal(board)

    # checking the loosing position. Penalize for every additional move
    if first:
        if len(all_1) == 0:
            return -1 - len(all_2)
    else:
        if len(all_2) == 0:
            return 1 + len(all_1)

    safe_1, safe_2 = extractSafeVertical(node), extractSafeHorizontal(node)
    num_t_1, tactic_1 = extractStrategicalVertical(node)
    num_t_2, tactic_2 = extractStrategicalHorizontal(node)

    set_1, set_2 = set(safe_1 + tactic_1), set(safe_2 + tactic_2)
    other_1 = [i for i in all_1 if i not in set_1]
    other_2 = [i for i in all_2 if i not in set_2]

    num_s_1, num_o_1, num_s_2, num_o_2 = len(safe_1), len(other_1), len(safe_2), len(other_2)

    value_1 = num_s_1 + num_t_1 / 2.0 + num_o_1 / 5.0
    value_2 = num_s_2 + num_t_2 / 2.0 + num_o_2 / 5.0

    print 'Position evaluation'
    print '\t', num_s_1, num_t_1, num_o_1
    print '\t', num_s_2, num_t_2, num_o_2
    print '\t', value_1, value_2
    print '\t', (value_1 - value_2)/(value_1 + value_2)

board = [
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]



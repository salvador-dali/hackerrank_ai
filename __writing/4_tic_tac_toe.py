from random import randint, choice

def isTerminal(node):
    return getHeuristicValue(node) is not None

def getHeuristicValue(node):
    """
    Node representation:
        0, 1, 2
        3, 4, 5
        6, 7 ,8
    node[0] where the X located
    node[1] where the O located
    :param node:
    :return:
    """
    winning = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},    # horizontal wins
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},    # vertical wins
        {0, 4, 8}, {2, 4, 6}                # diagonal wins
    ]

    # X wins
    if any(len(i.intersection(node[0])) == 3 for i in winning):
        return 1

    # O wins
    if any(len(i.intersection(node[1])) == 3 for i in winning):
        return -1

    # draw
    if len(node[0]) + len(node[1]) == 9:
        return 0

    return None

def getChildren(node):
    whoMoves = (len(node[0]) + len(node[1])) % 2
    whoStays = (whoMoves + 1) % 2
    left = {0, 1, 2, 3, 4, 5, 6, 7, 8} - node[0].union(node[1])

    children = []
    for pos in left:
        childNode = [0, 0]
        childNode[whoMoves] = node[whoMoves].copy().union({pos})
        childNode[whoStays] = node[whoStays].copy()
        children.append(tuple(childNode))
    return children

def negamax_with_move(node, depth, color):
    if depth == 0 or isTerminal(node):
        return color * getHeuristicValue(node), None

    bestValue, bestMove = float('-inf'), None
    for child in getChildren(node):
        val, _ = negamax_with_move(child, depth - 1, -color)
        m_val = -val
        if m_val > bestValue:
            bestValue, bestMove = m_val, [child]
        elif m_val == bestValue:
            bestMove.append(child)

    return bestValue, choice(bestMove)

# game logic

def findMove(node):
    if node is None:
        # X makes a random choice
        return 0, ({randint(0, 8)}, set([]))

    # check whether the position is real is a good idea
    X_pos, O_pos = node[0], node[1]
    total = len(X_pos) + len(O_pos)
    color = -1 if total % 2 else 1
    depth = 9 - total

    return negamax_with_move(node, depth, color)

# drawing

def drawBoard(node):
    board = ['_', '_', '_', '_', '_', '_', ' ', ' ', ' ']

    if node:
        for i in node[0]:
            board[i] = 'X'

        for i in node[1]:
            board[i] = 'O'

    print '|'.join(board[0:3])
    print '|'.join(board[3:6])
    print '|'.join(board[6:9])

def autoPlay():
    node = None
    for i in xrange(9):
        _, node = findMove(node)
        drawBoard(node)
        print

autoPlay()

from random import randint, choice

def isTerminal(node):
    return getHeuristicValue(node) is not None

def getHeuristicValue(node):
    winning = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    if any(len(i.intersection(node[0])) == 3 for i in winning):
        return 1

    if any(len(i.intersection(node[1])) == 3 for i in winning):
        return -1

    if len(node[0]) + len(node[1]) == 9:
        return 0

    return None

def getChildren(node):
    whoMoves = (len(node[0]) + len(node[1])) % 2
    whoStays = (whoMoves + 1) % 2

    children = []
    for pos in {0, 1, 2, 3, 4, 5, 6, 7, 8} - node[0].union(node[1]):
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

def findMove(node):
    if len(node[0]) + len(node[1]) == 0:
        return randint(0, 8)

    total = len(node[0]) + len(node[1])
    color = -1 if total % 2 else 1
    depth = 9 - total

    _, move = negamax_with_move(node, depth, color)
    X_values, O_values = move[0], move[1]
    d_x, d_o = list(X_values - node[0]), list(O_values - node[1])
    if len(d_x):
        return d_x[0]

    return d_o[0]

def representBoard(board):
    x_pos, o_pos = set([]), set([])
    for i in xrange(3):
        for j in xrange(3):
            if board[i][j] == 'X':
                x_pos.add(i*3 + j)
            elif board[i][j] == 'O':
                o_pos.add(i*3 + j)

    return x_pos, o_pos

board = [
    '___',
    '___',
    '___'
]
board = representBoard(board)
move = findMove(board)
print move
print move / 3, move % 3

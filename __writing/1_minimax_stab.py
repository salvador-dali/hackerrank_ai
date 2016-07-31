from random import choice

####################################################
#   These functions are needed in any algorithm
####################################################
def isTerminal(node):
    """ Tells whether the node is a terminal node.
    Terminal node is a win/draw/lose node

    :param node:
    :return: boolean
    """
    return True

def getHeuristicValue(node):
    """ For a node returns a value of it's position.
    The value for a win/draw/lose are hardcoded, other values reflect the
    likelihood of winning. The more accurate this function is, the better.

    :param node:
    :return: float
    """
    return 1

def getChildren(node):
    """ For a node position, it generates all the possible children of this node
    It is better to use a generator here, so that the values are generated only when needed.
    For minimax this can be just an array, but for alpha-beta where we will not search thought
    everything,  generator is preferred
    :param node:
    :return: a child of a node, till all children are generated
    """
    yield node

####################################################
#   Various algorithms
####################################################
def minimax(node, depth, isMaxPlayer):
    """ Starting from a Node, it finds the best solution for a tree with Depth.
    :param node:
    :param depth:
    :param isMaxPlayer:
    :return:
    """
    if depth == 0 or isTerminal(node):
        return getHeuristicValue(node)

    if isMaxPlayer:
        # bestValue = float('-inf')
        # for child in getChildren(node):
        #     bestValue = max(bestValue, minimax(child, depth - 1, False))
        # return bestValue
        return max(minimax(child, depth - 1, False) for child in getChildren(node))
    else:
        # bestValue = float('inf')
        # for child in getChildren(node):
        #     bestValue = min(bestValue, minimax(child, depth - 1, True))
        # return bestValue
        return min(minimax(child, depth - 1, True) for child in getChildren(node))


def negamax(node, depth, color):
    """ Does the same as minimax, but a little bit more concise.
    Relies on a fact that a game is zero sum

    Initial call for Player A's root node
    rootNegamaxValue := negamax( rootNode, depth, 1)
    rootMinimaxValue := rootNegamaxValue

    Initial call for Player B's root node
    rootNegamaxValue := negamax( rootNode, depth, -1)
    rootMinimaxValue := -rootNegamaxValue

    :param node:
    :param depth:
    :param color:
    :return:
    """
    if depth == 0 or isTerminal(node):
        return color * getHeuristicValue(node)

    # bestValue = float('-inf')
    # for child in getChildren(node):
    #     bestValue = max(bestValue, -negamax(child, depth - 1, -color))
    # return bestValue
    # or shorter and 1.25 times faster
    return max(-negamax(child, depth - 1, -color) for child in getChildren(node))


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


def alpha_beta(node, depth, a, b, isMaxPlayer):
    if depth == 0 or isTerminal(node):
        return getHeuristicValue(node)

    if isMaxPlayer:
        bestValue = float('-inf')
        for child in getChildren(node):
            bestValue = max(bestValue, alpha_beta(child, depth - 1, a, b, False))
            a = max(a, bestValue)
            if a > b:
                break
        return bestValue
    else:
        bestValue = float('inf')
        for child in getChildren(node):
            bestValue = min(bestValue, alpha_beta(child, depth - 1, a, b, True))
            b = min(b, bestValue)
            if a > b:
                break
        return bestValue


def alpha_beta_negamax(node, depth, a, b, color):
    """
    For a max player: alpha_beta_negamax(rootNode, depth, float('-inf'), float('inf'), 1)
    """
    if depth == 0 or isTerminal(node):
        return color * getHeuristicValue(node)

    bestValue = float('-inf')
    for child in getChildren(node):
        val = -alpha_beta_negamax(child, depth - 1, -b, -a, -color)
        bestValue = max(bestValue, val)
        a = max(a, val)
        if a >= b:
            break
    return bestValue


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
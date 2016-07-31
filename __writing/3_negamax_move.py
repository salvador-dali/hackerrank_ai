from random import randint, seed
seed(100)

# generate a tree helper methods

class Node():
    def __init__(self, data, children):
        self.data = data
        self.children = children

def generateTree(depth, branching):
    """
    generates a full tree with specific depth and branching factor.
    The values of the leaves are selected at random. They are returned as well.
    """
    total = branching**depth
    values = [randint(-10, 10) for i in xrange(total)]
    level = [Node(values[i], []) for i in xrange(total)]

    for _ in xrange(depth):
        total /= branching
        level = [Node(None, level[i * branching: (i+1) * branching]) for i in xrange(total)]

    return level[0], values

# helper functions for negamax

def isTerminal(node):
    return len(node.children) == 0

def getHeuristicValue(node):
    return node.data

def getChildren(node):
    return node.children

# negamax implementation

def negamax_with_move(node, depth, color):
    if depth == 0 or isTerminal(node):
        return color * getHeuristicValue(node), None

    bestValue, bestMove = float('-inf'), None
    for child in getChildren(node):
        val, _ = negamax_with_move(child, depth - 1, -color)
        if -val > bestValue:
            bestValue, bestMove = -val, child
    return bestValue, bestMove

# check how it works

depth, branching = 2, 3
tree, values = generateTree(depth, branching)

print values
val, move = negamax_with_move(tree, depth, 1)
print val

print [i.data for i in move.children]
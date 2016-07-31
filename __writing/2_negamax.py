# generate a tree helper methods

class Node():
    def __init__(self, data, children):
        self.data = data
        self.children = children

    def printChildrenValues(self, node):
        print [i.data for i in node.children]

def generateTree(depth, branching):
    """
    generates a full tree with specific depth and branching factor.
    The values of the leaves are selected at random. They are returned as well.
    """
    from random import randint, seed
    seed(2)
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

def negamax(node, depth, color):
    if depth == 0 or isTerminal(node):
        return color * getHeuristicValue(node)

    return max(-negamax(child, depth - 1, -color) for child in getChildren(node))

# check how it works

depth, branching = 2, 2
tree, values = generateTree(depth, branching)

print values
print negamax(tree, depth, 1)
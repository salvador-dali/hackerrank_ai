from random import randint, seed
from datetime import datetime
import matplotlib.pyplot as plt


class Node():
    def __init__(self, data, children):
        self.data = data
        self.children = children

    def printChildrenValues(self, node):
        print [i.data for i in node.children]

def generateTree(depth, branching):
    total = branching**depth
    values = [randint(-100, 100) for _ in xrange(total)]
    level = [Node(values[i], []) for i in xrange(total)]

    for _ in xrange(depth):
        total /= branching
        level = [Node(None, level[i * branching: (i+1) * branching]) for i in xrange(total)]

    return level[0], values


def isTerminal(node):
    return len(node.children) == 0

def getHeuristicValue(node):
    return node.data

def getChildren(node):
    return node.children


def alpha_beta_negamax(node, depth, a, b, color):
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

# ===================
def comparison():
    depth, branching = 15, 3
    tree, values = generateTree(depth, branching)

    startTime = datetime.now()
    print negamax(tree, depth, 1)
    print datetime.now() - startTime

    startTime = datetime.now()
    print alpha_beta_negamax(tree, depth, float('-inf'), float('inf'), 1)
    print datetime.now() - startTime


def longComparison(d_start, d_end, branching):
    x = range(d_start, d_end + 1)
    y_minimax, y_alpha_beta = [], []
    for i in x:
        depth = i
        tree, values = generateTree(depth, branching)

        startTime = datetime.now()
        v1 = negamax(tree, depth, 1)
        t1 = int((datetime.now() - startTime).microseconds)

        startTime = datetime.now()
        v2 = alpha_beta_negamax(tree, depth, float('-inf'), float('inf'), 1)
        t2 = int((datetime.now() - startTime).microseconds)
        if v1 != v2:
            print 'Epic fail, they should be equal'
            break
        y_minimax.append(t1)
        y_alpha_beta.append(t2)

    plt.plot(x, y_minimax, 'bs-', x, y_alpha_beta, 'g^-')
    plt.title('b = ' + str(branching), fontsize=20)
    # plt.yscale('log', nonposy='clip')
    plt.show()

longComparison(1, 6, 12)





from random import randint, seed, choice
seed(2)

class Node():
    def __init__(self, data, children, is_chance, probabilities=None):
        self.data = data
        self.children = children
        self.isChance = is_chance
        if is_chance:
            self.probabilities = probabilities

def generateProbabilities(l):
    s = 0
    while s == 0:
        arr = [randint(0, 10) for i in xrange(l)]
        s = float(sum(arr))

    return [i / s for i in arr]

def generateTreeWithChance(depth, branching):
    total = branching ** (depth * 2)
    values = [randint(-10, 10) for _ in xrange(total)]
    is_chance = False
    level = [Node(values[i], [], is_chance) for i in xrange(total)]

    for _ in xrange(depth * 2):
        total /= branching
        is_chance = not is_chance
        if is_chance:
            prob = [generateProbabilities(branching) for _ in xrange(total)]
            level = [Node(None, level[i * branching: (i+1) * branching], True, prob[i]) for i in xrange(total)]
        else:
            level = [Node(None, level[i * branching: (i+1) * branching], False) for i in xrange(total)]

    return level[0], values

# ==========================================

def isTerminal(node):
    return len(node.children) == 0

def getHeuristicValue(node):
    return node.data

def getChildren(node):
    return node.children

def getType(current_depth, color=1):
    if current_depth % 2 == 1:
        return 0    # chance node
    return color * (-1 if current_depth / 2 % 2 == 1 else 1)

def expectiminimax(node, depth, max_depth, color):
    current_depth = max_depth - depth
    if depth == 0 or isTerminal(node):
        return getHeuristicValue(node), [None]

    if getType(current_depth, color) == -1:
        best_value, best_move = float('inf'), []
        for child in getChildren(node):
            tmp_value, _ = expectiminimax(child, depth - 1, max_depth, color)
            if tmp_value < best_value:
                best_move, best_value = [child], tmp_value
            elif tmp_value == best_value:
                best_move.append(child)
    elif getType(current_depth, color) == 1:
        best_value, best_move = float('-inf'), []
        for child in getChildren(node):
            tmp_value, _ = expectiminimax(child, depth - 1, max_depth, color)
            if tmp_value > best_value:
                best_move, best_value = [child], tmp_value
            elif tmp_value == best_value:
                best_move.append(child)
    else:
        children, probabilities = getChildren(node), node.probabilities
        return sum(p * expectiminimax(c, depth - 1, max_depth, color)[0] for p, c in zip(probabilities, children)), None

    return best_value, choice(best_move)


depth, branch = 2, 30
tree, values = generateTreeWithChance(depth, branch)
val, node = expectiminimax(tree, depth * 2, depth * 2, 1)

print val
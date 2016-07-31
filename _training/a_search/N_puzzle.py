from copy import deepcopy
from Queue import PriorityQueue


def manhattan(s, e):
    # manhattan distance between two states
    return abs(s[0] - e[0]) + abs(s[1] - e[1])


def heuristic(board):
    # this heuristics is admissible and consistent
    # h(n) is equal to the sum of distances of each number to its goal position
    l, s = len(board), 0
    for i in xrange(l):
        for j in xrange(l):
            m = board[i][j]
            if m:
                s += manhattan((i, j), (m / l, m % l))
    return s


def board2state(board):
    # convert the current board position to a hashable string
    out = []
    for i in board:
        out += i

    return '_'.join(map(str, out))


def state2board(board_encoded):
    # convert the hashable string into a board position
    out = map(int, board_encoded.split('_'))
    l = int(len(out)**0.5)
    res = []
    for i in zip(*[iter(out)] * l):
        res.append(list(i))

    return res


def generatePossibleStates(board):
    # generates all possible new states from the current board
    out, states = [], []
    for i in board:
        out += i

    pos = out.index(0)
    i, j = pos / len(board), pos % len(board)
    if i > 0:
        # UP
        state = deepcopy(board)
        state[i - 1][j] = 0
        state[i][j] = board[i - 1][j]
        states.append((state, 'UP'))
    if i < len(board) - 1:
        # DOWN
        state = deepcopy(board)
        state[i + 1][j] = 0
        state[i][j] = board[i + 1][j]
        states.append((state, 'DOWN'))
    if j > 0:
        # LEFT
        state = deepcopy(board)
        state[i][j - 1] = 0
        state[i][j] = board[i][j - 1]
        states.append((state, 'LEFT'))
    if j < len(board) - 1:
        # RIGHT
        state = deepcopy(board)
        state[i][j + 1] = 0
        state[i][j] = board[i][j + 1]
        states.append((state, 'RIGHT'))

    return states


def printBoard(board):
    # helper to print the board
    for i in board:
        print ' '.join(map(str, i))


def N_puzzle(startPosition):
    frontier, pos_encoded = PriorityQueue(), board2state(startPosition)
    frontier.put((0, pos_encoded))
    parent, backtracking, checked = None, {pos_encoded: [None, None]}, set([pos_encoded])

    endPosition = '_'.join(map(str, range(len(startPosition)**2)))
    while not frontier.empty():
        cost, pos_encoded = frontier.get()
        direction = None
        if pos_encoded == endPosition:
            parent = [pos_encoded, None]
            break

        pos_decoded = state2board(pos_encoded)
        states = generatePossibleStates(pos_decoded)
        for i in states:
            state, direction = i
            pos_encoded_new = board2state(state)
            if pos_encoded_new not in checked:
                checked.add(pos_encoded_new)
                backtracking[pos_encoded_new] = [pos_encoded, direction]
                frontier.put((heuristic(state), pos_encoded_new))

    out = []
    while parent[0] is not None:
        out.append(parent)
        parent = backtracking[parent[0]]

    return out[::-1]


board = [
    [0, 3, 8],
    [4, 1, 7],
    [2, 6, 5]
]
l = N_puzzle(board)
print len(l)
for i in l:
    printBoard(state2board(i[0]))
    print i[1]
    print
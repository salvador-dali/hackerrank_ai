from Queue import PriorityQueue
def heuristic(s, e):
    return abs(s[0] - e[0]) + abs(s[1] - e[1])

def A_star(board, start, end):
    def addToFrontierIfOk(y_, x_):
        # check whether the point is inside of the board, is not
        # in the wall. So if everything is OK, then add it to the frontier
        # to the list of checked and backtracking
        if board[y_][x_] != '%':
            i = y_ * m + x_
            if i not in checked:
                cost_ = 1 + heuristic((y_, x_), end)
                frontier.put((cost_, y_, x_))
                checked.add(i)
                backtracking[i] = prevIndex

    n, m, frontier, y, x = len(board), len(board[0]), PriorityQueue(), start[0], start[1]
    frontier.put((0, y, x))
    index = y * m + x
    parent, backtracking, checked = None, {index: None}, set([index])

    while not frontier.empty():
        cost, y, x = frontier.get()
        #print 'Expanding this point: (', y, x, ') with cost:', cost
        prevIndex = y * m + x
        if (y, x) == end:
            parent = prevIndex
            break

        if y > 0: addToFrontierIfOk(y - 1, x)
        if x > 0: addToFrontierIfOk(y, x - 1)
        if x < m: addToFrontierIfOk(y, x + 1)
        if y < m: addToFrontierIfOk(y + 1, x)

    out = []
    while parent is not None:
        out.append((parent / m, parent % m))
        parent = backtracking[parent]

    return out[::-1]

start = (35, 35)
end = (35, 1)
board = [
    '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
    '%-------%-%-%-----------%---%-----%-%',
    '%-%%%%%%%-%-%%%-%-%%%-%%%-%%%%%%%-%-%',
    '%-------%-------%-%-----%-----%-%---%',
    '%%%%%-%%%%%-%%%-%-%-%-%%%-%%%%%-%-%%%',
    '%---%-%-%-%---%-%-%-%---%-%---%-%---%',
    '%-%%%-%-%-%-%%%-%%%%%-%%%-%-%%%-%%%-%',
    '%-------%-----%---%---%-----%-%-%---%',
    '%%%-%%%%%%%%%-%%%%%%%-%%%-%%%-%-%-%-%',
    '%-------------%-------%-%---%-----%-%',
    '%-%-%%%%%-%-%%%-%-%-%%%-%-%%%-%%%-%-%',
    '%-%-%-----%-%-%-%-%-----%---%-%-%-%-%',
    '%-%-%-%%%%%%%-%-%%%%%%%%%-%%%-%-%%%-%',
    '%-%-%-%-----%---%-----%-----%---%---%',
    '%%%-%%%-%-%%%%%-%%%%%-%%%-%%%-%%%%%-%',
    '%-----%-%-%-----%-%-----%-%---%-%-%-%',
    '%-%-%-%-%-%%%-%%%-%%%-%%%-%-%-%-%-%-%',
    '%-%-%-%-%-----------------%-%-%-----%',
    '%%%-%%%%%%%-%-%-%%%%%-%%%-%-%%%-%%%%%',
    '%-------%-%-%-%-----%---%-----%-%---%',
    '%%%%%-%-%-%%%%%%%%%-%%%%%%%%%%%-%-%%%',
    '%---%-%-----------%-%-----%---%-%---%',
    '%-%%%-%%%%%-%%%%%%%%%-%%%%%-%-%-%%%-%',
    '%-%---%------%--------%-----%-------%',
    '%-%-%-%%%%%-%%%-%-%-%-%-%%%%%%%%%%%%%',
    '%-%-%---%-----%-%-%-%-------%---%-%-%',
    '%-%-%%%-%%%-%-%-%-%%%%%%%%%-%%%-%-%-%',
    '%-%---%-%---%-%-%---%-%---%-%-%-----%',
    '%-%%%-%%%-%%%%%-%%%-%-%-%%%%%-%-%%%%%',
    '%-------%---%-----%-%-----%---%-%---%',
    '%%%-%-%%%%%-%%%%%-%%%-%%%-%-%%%-%-%%%',
    '%-%-%-%-%-%-%-%-----%-%---%-%---%-%-%',
    '%-%-%%%-%-%-%-%-%%%%%%%%%-%-%-%-%-%-%',
    '%---%---%---%-----------------%-----%',
    '%-%-%-%-%%%-%%%-%%%%%%%-%%%-%%%-%%%-%',
    '%.%-%-%-------%---%-------%---%-%--P%',
    '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
]
l = A_star(board, start, end)
print len(l) - 1
for i in l:
    print i[0], i[1]
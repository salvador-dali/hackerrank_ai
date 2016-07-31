from Queue import Queue
def findSolution(board, start, end):
    def addToFrontierIfOk(y_, x_):
        if board[y_][x_] != '%':
            i = y_ * m + x_
            if i not in checked:
                frontier.put((y_, x_))
                checked.add(i)
                backtracking[i] = prevIndex

    n, m, frontier = len(board), len(board[0]), Queue()
    frontier.put(start)

    index = start[0] * m + start[1]
    parent, backtracking, checked = None, {index: None}, set([index])

    stupidity = []
    while not frontier.empty():
        y, x = frontier.get()
        prevIndex = y * m + x
        stupidity.append((y, x))
        if (y, x) == end:
            parent = prevIndex
            break

        if y > 0: addToFrontierIfOk(y - 1, x)
        if x > 0: addToFrontierIfOk(y, x - 1)
        if x < m: addToFrontierIfOk(y, x + 1)
        if y < m: addToFrontierIfOk(y + 1, x)

    print len(stupidity)
    for i in stupidity:
        print i[0], i[1]

    out = []
    while parent is not None:
        out.append((parent / m, parent % m))
        parent = backtracking[parent]

    return out[::-1]




start = (3, 9)
end = (5, 1)
board = [
    '%%%%%%%%%%%%%%%%%%%%',
    '%--------------%---%',
    '%-%%-%%-%%-%%-%%-%-%',
    '%--------P-------%-%',
    '%%%%%%%%%%%%%%%%%%-%',
    '%.-----------------%',
    '%%%%%%%%%%%%%%%%%%%%'
]
board = [
    #01234567890123456789
    '%%%%%%%%%%%%%%%%%%%%',  #0
    '%--------------%---%',  #1
    '%-%%-%%-%%-%%-%%-%-%',  #2
    '%--------P-------%-%',  #3
    '%%%%%%%%%%%%%%%%%%-%',  #4
    '%.-----------------%',  #5
    '%%%%%%%%%%%%%%%%%%%%'   #6
]

l = findSolution(board, start, end)
print len(l) - 1
for i in l:
    print i[0], i[1]
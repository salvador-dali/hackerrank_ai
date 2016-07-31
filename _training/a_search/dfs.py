def findSolution(board, start, end):
    n, m = len(board), len(board[0])

    frontier = [(start[0], start[1], None)]
    parent = None
    backtracking = {}
    checked = set()

    stupidity = []
    while len(frontier):
        y, x, prev = frontier.pop()
        index = y * m + x
        backtracking[index] = prev
        checked.add(index)
        stupidity.append(index)

        if (y, x) == end:
            parent = index
            break
        #print y, x

        if y > 0 and board[y - 1][x] != '%' and (y - 1) * m + x not in checked:
            # UP
            frontier.append((y - 1, x, index))
        if x > 0 and board[y][x - 1] != '%' and y * m + (x - 1) not in checked:
            # LEFT
            frontier.append((y, x - 1, index))
        if x < m and board[y][x + 1] != '%' and y * m + (x + 1) not in checked:
            # RIGHT
            frontier.append((y, x + 1, index))
        if y < m and board[y + 1][x] != '%' and (y + 1) * m + x not in checked:
            # DOWN
            frontier.append((y + 1, x, index))

    out = []
    while parent is not None:
        out.append((parent / m, parent % m))
        parent = backtracking[parent]

    return stupidity, out[::-1]


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
stupidity, path = findSolution(board, start, end)
print len(stupidity)
for i in stupidity:
    print i / len(board), i % len(board)

print len(path) - 1
for i in path:
    print i[0], i[1]
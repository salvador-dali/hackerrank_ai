from AI_helper import move2DGrid, manhattan, TSP
def find_all(a_str, sub):
    start, positions = 0, []
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return positions
        positions.append(start)
        start += len(sub)
    return positions

def botFinding(y, x, M):
    points = []
    for i in xrange(len(M)):
        find_all(M[i], 'd')
        for j in find_all(M[i], 'd'):
            points.append([i, j])

    tour = TSP([y, x], points, manhattan)
    return move2DGrid([y, x], tour[0])

arr = [
    '----d',
    '--d-d',
    '--dd-',
    '--d--',
    '----d'
]

print botFinding(1, 0, arr)
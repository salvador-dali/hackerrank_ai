from AI_helper import move2DGrid
def botFinding(bot, M):
    for i in xrange(5):
        line = M[i]
        j = line.find('d')
        if j != -1:
            target = [i, j]
            break

    if bot[0] == target[0] and bot[1] == target[1]:
        return 'CLEAN'
    return move2DGrid(bot, target)

arr = [
    'b---d',
    '-----',
    '-----',
    '-----',
    '-----'
]
print botFinding([0, 0], arr)

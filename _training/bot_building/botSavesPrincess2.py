from AI_helper import move2DGrid
def botFinding(M):
    l, princes, bot = len(M), None, None
    for i in xrange(l):
        line = M[i]
        tmp1, tmp2 = line.find('p'), line.find('m')

        if tmp1 != -1:
            princes = [i, tmp1]
        if tmp2 != -1:
            bot = [i, tmp2]

        # we already found both positions
        if princes and bot:
            break

    return move2DGrid(bot, princes)

arr = [
    '-----',
    '-----',
    '---m-p',
    '-----',
    '-----'
]
print botFinding(arr)
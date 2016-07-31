def botFinding(M):
    l = len(M)
    # find in which of the corners the Princess is
    if M[0][0] == 'p':
        pos1, pos2 = 'LEFT', 'TOP'
    elif M[0][l - 1] == 'p':
        pos1, pos2 = 'RIGHT', 'TOP'
    elif M[l - 1][0] == 'p':
        pos1, pos2 = 'LEFT', 'DOWN'
    else:
        pos1, pos2 = 'RIGHT', 'DOWN'

    # standing in the exact center it is not hard to count the number
    # of moves needed to go there
    num = l / 2
    return [pos1] * num + [pos2] * num

for i in botFinding(['---', '-m-', 'p--']):
    print i
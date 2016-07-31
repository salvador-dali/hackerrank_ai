from random import random
def generateValue(prob):
    s, n = 0, random()
    for i in xrange(len(prob)):
        s += prob[i]
        if n < s:
            return i + 1

def markov(prob, ladders):
    position, steps = 1, 0
    while position != 100:
        dieChoice = generateValue(prob)
        steps += 1
        tmp = position + dieChoice
        if tmp <= 100:
            position = tmp
            if tmp in ladders:
                position = ladders[tmp]

    return steps

def simulate(prob, ladders, n=5000):
    s, k = 0.0, 0
    for i in xrange(n):
        z = markov(prob, ladders)
        if z <= 1000:
            s += z
            k += 1

    return s / k

prob = [0.32, 0.32, 0.12, 0.04, 0.07, 0.13]
ladders = {
    32: 62,
    42: 68,
    12: 98,
    95: 13,
    97: 25,
    93: 37,
    79: 27,
    75: 19,
    49: 47,
    67: 17
}

simulate(prob, ladders)
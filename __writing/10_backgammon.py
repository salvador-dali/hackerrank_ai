node = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0, 0]


def possibleMoves(node, rolls):
    # if dices[0] == dices[1]:
    #     throws = [dices[0]] * 4
    # else:
    #     throws = [dices[0], dices[1], dices[0] + dices[1]]
    # print 'Your throws:\t\t', throws
    # starts = [(pos, val) for pos, val in enumerate(node['board']) if val >= node['move']]

    for pos in xrange(24):
        if node[pos] > 0:
            new_pos = pos + rolls[0]
            if node[new_pos] == -1:
                # hit the piece of the opponent
                node_copy = node[::]
                node_copy[new_pos] = 1
                pass
            elif node[new_pos] >= 0:
                # your piece or empty
                node_copy = node[::]
                node_copy[new_pos] += 1
                pass

            node_copy[pos] -= 1


            print node_copy



# possibleMoves(node, (2, 6))


def expected(probabilities, values):
    print sum(p * v for p, v in zip(probabilities, values))

expected(
    [0.2, 0.8],
    [1, -1.5]
)
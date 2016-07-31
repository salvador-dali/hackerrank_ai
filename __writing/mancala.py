# is_first = input() == 1
# mancala_1, holes_1 = input(), [int(i) for i in raw_input().strip().split()]
# mancala_2, holes_2 = input(), [int(i) for i in raw_input().strip().split()]
from random import choice
from datetime import datetime
from collections import Counter

class AgentBase():
    def printMancala(self, arr, is_first):
        holes_1, holes_2, mancala_1, mancala_2 = arr[0:6], arr[7:13], arr[6], arr[13]
        print '  ', 'First (bottom)' if is_first else 'Second (top)', 'player to move'
        print '------------------------------------'
        print 'P2  |\t' + '\t'.join(map(str, holes_2[::-1])), '\t|'
        print str(mancala_2), '\t|                           |', str(mancala_1)
        print '\t|\t' + '\t'.join(map(str, holes_1)), '\t| P1'
        print '------------------------------------\n\n'

    def makeMove(self, arr, is_first, pos):
        if is_first:
            is_first, stones, arr[pos] = False, arr[pos], 0
            while stones > 0:
                if pos == 12: pos = -1
                pos += 1
                arr[pos] += 1
                stones -= 1

            if arr[pos] - 1 == 0 and pos < 6:
                # If the last marble you drop is in an empty hole on your side, you empty all marbles
                # on the hole directly opposite to your hole and put it in your hole.
                arr[pos] += arr[12 - pos]
                arr[12 - pos] = 0
            elif pos == 6:
                # If the last marble you drop is in your own mancala, you get a free turn.
                is_first = True

            if sum(arr[0:6]) == 0:
                return arr, False

            return arr, is_first
        else:
            is_first, pos = True, pos + 7
            stones, arr[pos] = arr[pos], 0
            while stones > 0:
                if pos == 13:
                    pos = -1
                elif pos == 5:
                    pos = 6
                pos += 1
                arr[pos] += 1
                stones -= 1

            if arr[pos] - 1 == 0 and 6 < pos < 13:
                # If the last marble you drop is in an empty hole on your side, you empty all marbles
                # on the hole directly opposite to your hole and put it in your hole.
                arr[pos] += arr[12 - pos]
                arr[12 - pos] = 0
            elif pos == 13:
                # If the last marble you drop is in your own mancala, you get a free turn.
                is_first = False

            if sum(arr[7:13]) == 0:
                return arr, True

            return arr, is_first

    def isTerminal(self, arr):
        return sum(arr[0:6]) == 0 or sum(arr[7:13]) == 0

    def generateMovesFirst(self, arr, original_move, all_pos):
        for move in xrange(6):
            if not arr[move]:
                continue

            board, is_first = self.makeMove(arr[::], True, move)
            if not is_first:
                all_pos.append((original_move if original_move is not None else move, (board, is_first)))
            else:
                self.generateMovesFirst(board, original_move if original_move is not None else move, all_pos)

    def generateMovesSecond(self, arr, original_move, all_pos):
        for move in xrange(7, 13):
            if not arr[move]:
                continue

            move -= 7
            board, is_first = self.makeMove(arr[::], False, move)
            if is_first:
                all_pos.append((original_move if original_move is not None else move, (board, is_first)))
            else:
                self.generateMovesSecond(board, original_move if original_move is not None else move, all_pos)

    def generateMoves(self, arr, is_first):
        all_pos = []
        func = self.generateMovesFirst if is_first else self.generateMovesSecond
        func(arr, None, all_pos)

        if is_first:
            all_pos.sort(key=lambda x: -x[1][0][6])
        else:
            all_pos.sort(key=lambda x: -x[1][0][13])

        return all_pos

    def whoWon(self, arr):
        p1, p2 = sum(arr[0:6]), sum(arr[7:13])
        if p1 == 0 or p2 == 0:
            return cmp(p1 + arr[6], p2 + arr[13])
        return None


class AgentRandom(AgentBase):
    def getBestMove(self, arr, is_first):
        if is_first:
            moves = [move for move in xrange(0, 6) if arr[move]]
        else:
            moves = [move - 7 for move in xrange(7, 13) if arr[move]]

        return choice(moves)


class AgentSimple(AgentBase):
    def evaluation(self, arr, is_first, is_debug=False):
        p1, p2 = sum(arr[0:6]), sum(arr[7:13])
        if p1 == 0 or p2 == 0:
            # the game ended
            res1, res2 = p1 + arr[6], p2 + arr[13]
            if is_debug:
                print res1, res2
            return cmp(res1, res2) * 100
        return arr[6] - arr[13]

    def alpha_beta(self, arr, depth, a, b, color, f_eval):
        if depth == 0 or self.isTerminal(arr):
            return color * f_eval(arr, True if color == 1 else False), None

        best_value, best_moves, is_first = float('-inf'), [], True if color == 1 else False
        for tmp in self.generateMoves(arr, is_first):
            move, child = tmp[0], tmp[1][0]
            val, _ = self.alpha_beta(child, depth - 1, -b, -a, -color, f_eval)
            m_val = - val
            if m_val > best_value:
                best_value, best_moves = m_val, [move]
            elif m_val == best_value:
                best_moves.append(move)

            a = max(a, m_val)
            if a >= b:
                break

        return best_value, choice(best_moves)

    def getBestMove(self, arr, is_first):
        color = 1 if is_first else -1
        return self.alpha_beta(arr, 6, float('-inf'), float('inf'), color, self.evaluation)[1]


class AgentImproved(AgentSimple):
    def __init__(self, param):
        self.param = param

    def evaluation(self, arr, is_first, is_debug=False):
        p1, p2 = sum(arr[0:6]), sum(arr[7:13])
        if p1 == 0 or p2 == 0:
            res1, res2 = p1 + arr[6], p2 + arr[13]
            if is_debug:
                print res1, res2
            return cmp(res1, res2) * 100
        return arr[6] - arr[13] + (p1 - p2) / self.param


class Competition():
    def playGame(self, player1, player2, is_debug=False):
        arr, is_first, is_finished = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0], True, False
        while not is_finished:
            move = (player1 if is_first else player2).getBestMove(arr, is_first)
            arr, is_first = player1.makeMove(arr, is_first, move)
            is_finished = player1.isTerminal(arr)
            if is_debug: player1.printMancala(arr, is_first)

        return player1.whoWon(arr)

    def face2face(self, player1, player2, rounds, debugger=False):
        res1 = Counter(self.playGame(player1, player2) for _ in xrange(rounds))
        if debugger:
            print "Player1 vs Player2 (W/D/L): \033[1m%s/%s/%s\033[0m" % (res1[1], res1[0], res1[-1])
        res2 = Counter(self.playGame(player2, player1) for _ in xrange(rounds))
        if debugger:
            print "Player2 vs Player1 (W/D/L): \033[1m%s/%s/%s\033[0m" % (res2[1], res2[0], res2[-1])
        fitness = 3.0 * (res1[1] - res2[1]) + res1[0] - res2[0]

        # the value is always between [-3; 3]. Close to 0 means that players are almost the
        # same strength. The closer to -3, the more first player weaker than the second.
        return fitness / rounds

    def tournament(self, rounds, *players):
        def helper(i, j, results):
            if i == j:
                return '{: ^5}'.format('x')

            res = results[min(i, j), max(i, j)]
            if i < j:
                return '{: ^5}'.format(res)
            else:
                return '{: ^5}'.format(-res)


        def getTotal(row):
            total = 0
            for i in row:
                if i.strip() != 'x':
                    total += float(i.strip())
            return total

        l = len(players)
        results = {(i, j): self.face2face(players[i], players[j], rounds) for i in xrange(l) for j in xrange(i + 1, l)}

        print results

        table = [[helper(i, j, results) for j in xrange(l)] for i in xrange(l)]

        for row in table:
            print '\t\t'.join(row) + '   |  ' + '{: ^5}'.format(getTotal(row))


totalGames = 5
c = Competition()

# player1, player2, player3 = AgentRandom(), AgentSimple(), AgentImproved()
player1, player2, player3, player4, player5, player6 = AgentSimple(), AgentImproved(7), AgentImproved(7.5), AgentImproved(8), AgentImproved(8.5), AgentImproved(9)
startTime = datetime.now()
c.tournament(totalGames, player1, player2, player3, player4, player5, player6)
print datetime.now() - startTime

# player1, player2, player3, player4, player5, player6 = AgentSimple(), AgentImproved(1), AgentImproved(2), AgentImproved(5), AgentImproved(7.5), AgentImproved(10)
# {(0, 1): -0.368, (1, 2): 0.228, (2, 5): 0.814, (1, 3): 1.03, (4, 5): 1.334, (1, 4): -1.274, (2, 4): -1.034, (1, 5): 0.958, (0, 5): 0.058, (0, 4): -1.386, (2, 3): 0.818, (0, 3): -0.24, (3, 4): -1.092, (0, 2): -0.594, (3, 5): 0.32}
#   x  		-0.368		-0.594		-0.24		-1.386		0.058   |  -2.53
# 0.368		  x  		0.228		1.03 		-1.274		0.958   |  1.31
# 0.594		-0.228		  x  		0.818		-1.034		0.814   |  0.964
# 0.24 		-1.03		-0.818		  x  		-1.092		0.32    |  -2.38
# 1.386		1.274		1.034		1.092		  x  		1.334   |  6.12
# -0.058		-0.958		-0.814		-0.32		-1.334		  x     |  -3.484
# 18:56:01.871332


# player1, player2, player3, player4, player5, player6 = AgentSimple(), AgentImproved(7), AgentImproved(7.5), AgentImproved(8), AgentImproved(8.5), AgentImproved(9)
# {(0, 1): -0.01, (1, 2): -1.29, (2, 5): 1.17, (1, 3): -0.044, (4, 5): 1.32, (1, 4): -1.17, (2, 4): 0.142, (1, 5): 0.054, (0, 5): -0.24, (0, 4): -1.382, (2, 3): 1.312, (0, 3): -0.176, (3, 4): -1.38, (0, 2): -1.484, (3, 5): -0.01}
#   x  		-0.01		-1.484		-0.176		-1.382		-0.24   |  -3.292
# 0.01 		  x  		-1.29		-0.044		-1.17		0.054   |  -2.44
# 1.484		1.29 		  x  		1.312		0.142		1.17    |  5.398
# 0.176		0.044		-1.312		  x  		-1.38		-0.01   |  -2.482
# 1.382		1.17 		-0.142		1.38 		  x  		1.32    |  5.11
# 0.24 		-0.054		-1.17		0.01 		-1.32		  x     |  -2.294
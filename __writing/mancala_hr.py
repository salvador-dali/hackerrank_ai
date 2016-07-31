# is_first = input() == 1
# mancala_1, holes_1 = input(), [int(i) for i in raw_input().strip().split()]
# mancala_2, holes_2 = input(), [int(i) for i in raw_input().strip().split()]
from random import choice
from datetime import datetime
startTime = datetime.now()



class AgentImproved():
    def __init__(self, param, depth):
        self.param = param
        self.depth = depth

    def makeMove(self, arr, is_first, pos):
        if is_first:
            is_first, stones, arr[pos] = False, arr[pos], 0
            while stones > 0:
                if pos == 12: pos = -1
                pos += 1
                arr[pos] += 1
                stones -= 1

            if arr[pos] - 1 == 0 and pos < 6:
                arr[pos] += arr[12 - pos]
                arr[12 - pos] = 0
            elif pos == 6:
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
                arr[pos] += arr[12 - pos]
                arr[12 - pos] = 0
            elif pos == 13:
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

    def alpha_beta(self, arr, depth, a, b, color, f_eval):
        if depth == 0 or self.isTerminal(arr):
            return color * f_eval(arr), None

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
        return self.alpha_beta(arr, self.depth, float('-inf'), float('inf'), color, self.evaluation)[1]

    def evaluation(self, arr):
        p1, p2 = sum(arr[0:6]), sum(arr[7:13])
        if p1 == 0 or p2 == 0:
            res1, res2 = p1 + arr[6], p2 + arr[13]
            return cmp(res1, res2) * 100
        return arr[6] - arr[13] + (p1 - p2) / self.param


is_first = True
arr = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

player1 = AgentImproved(7.5, 8)
player2 = AgentImproved(7.5, 8)
move = (player1 if is_first else player2).getBestMove(arr, is_first)
print move
arr, is_first = player1.makeMove(arr, is_first, move)

print datetime.now() - startTime
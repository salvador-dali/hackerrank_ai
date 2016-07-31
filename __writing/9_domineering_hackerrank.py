from random import choice
from datetime import datetime
n = 8

class AgentGoodFaster():
    def nodeToBoard(self, node):
        arr = [int(i) for i in bin(node)[2:].zfill(n*n)]
        return [arr[n*i:n*i+n] for i in xrange(n)]

    def boardToNode(self, board):
        return int(''.join([str(item) for line in board for item in line]), 2)

    def isVertical(self, board):
        return sum(item for line in board for item in line) / 2 % 2 == 0

    def isTerminal(self, node):
        board = self.nodeToBoard(node)
        if self.isVertical(board):
            return not any(board[i][j] + board[i + 1][j] == 0 for j in xrange(n) for i in xrange(n - 1))

        return not any(board[i][j] + board[i][j + 1] == 0 for j in xrange(n - 1) for i in xrange(n))

    def printBoard(self, node):
        for line in self.nodeToBoard(node):
            print ''.join(['x' if i else '.' for i in line])
        print

    def alpha_beta_general(self, node, depth, a, b, color, f_get_children, f_eval):
        if depth == 0 or self.isTerminal(node):
            return color * f_eval(node), None

        bestValue, bestMoves = float('-inf'), []
        for child in f_get_children(node):
            val, _ = self.alpha_beta_general(child, depth - 1, -b, -a, -color, f_get_children, f_eval)
            m_val = - val
            if m_val > bestValue:
                bestValue, bestMoves = m_val, [child]
            elif m_val == bestValue:
                bestMoves.append(child)

            a = max(a, m_val)
            if a >= b:
                break
        return bestValue, choice(bestMoves)

    def getMovesV(self, board):
        children = []
        for i in xrange(n - 1):
            for j in xrange(n):
                if board[i][j] + board[i + 1][j] == 0:
                    board[i][j], board[i + 1][j] = 1, 1
                    children.append(self.boardToNode(board))
                    board[i][j], board[i + 1][j] = 0, 0
        return children

    def getMovesH(self, board):
        children = []
        for i in xrange(n):
            for j in xrange(n - 1):
                if board[i][j] + board[i][j + 1] == 0:
                    board[i][j], board[i][j + 1] = 1, 1
                    children.append(self.boardToNode(board))
                    board[i][j], board[i][j + 1] = 0, 0
        return children

    def getMoves(self, node):
        board = self.nodeToBoard(node)
        if self.isVertical(board):
            return self.getMovesV(board)

        return self.getMovesH(board)

    def isSafeV(self, board, i, j):
        if j == 0:
            if board[i][j + 1] and board[i + 1][j + 1]:
                return True
        elif j == n - 1:
            if board[i][j - 1] and board[i + 1][j - 1]:
                return True
        elif board[i][j + 1] and board[i + 1][j + 1] and board[i][j - 1] and board[i + 1][j - 1]:
            return True

        return False

    def isSafeH(self, board, i, j):
        if i == 0:
            if board[i + 1][j] and board[i + 1][j + 1]:
                return True
        elif i == n - 1:
            if board[i - 1][j] and board[i - 1][j + 1]:
                return True
        elif board[i + 1][j] and board[i + 1][j + 1] and board[i - 1][j] and board[i - 1][j + 1]:
            return True

        return False

    def getSafeV(self, node):
        board_modify, board_copy, moves = self.nodeToBoard(node), self.nodeToBoard(node), []
        for i in xrange(n - 1):
            for j in xrange(n):
                if not board_modify[i][j] and not board_modify[i + 1][j] and self.isSafeV(board_modify, i, j):
                    board_modify[i][j], board_modify[i + 1][j] = 1, 1
                    board_copy[i][j], board_copy[i + 1][j] = 1, 1
                    moves.append(self.boardToNode(board_copy))
                    board_copy[i][j], board_copy[i + 1][j] = 0, 0

        return moves

    def getSafeH(self, node):
        board_modify, board_copy, moves = self.nodeToBoard(node), self.nodeToBoard(node), []
        for i in xrange(n):
            for j in xrange(n - 1):
                if not board_modify[i][j] and not board_modify[i][j + 1] and self.isSafeH(board_modify, i, j):
                    board_modify[i][j], board_modify[i][j + 1] = 1, 1
                    board_copy[i][j], board_copy[i][j + 1] = 1, 1
                    moves.append(self.boardToNode(board_copy))
                    board_copy[i][j], board_copy[i][j + 1] = 0, 0

        return moves

    def isTacticV(self, board, i, j):
        moves = []

        board[i][j], board[i + 1][j] = 1, 1
        if self.isSafeV(board, i, j + 1):
            moves.append(self.boardToNode(board))
        board[i][j], board[i + 1][j] = 0, 0

        board[i][j + 1], board[i + 1][j + 1] = 1, 1
        if self.isSafeV(board, i, j):
            moves.append(self.boardToNode(board))
        board[i][j + 1], board[i + 1][j + 1] = 0, 0

        return moves

    def isTacticH(self, board, i, j):
        moves = []

        board[i][j], board[i][j + 1] = 1, 1
        if self.isSafeH(board, i + 1, j):
            moves.append(self.boardToNode(board))
        board[i][j], board[i][j + 1] = 0, 0

        board[i + 1][j], board[i + 1][j + 1] = 1, 1
        if self.isSafeH(board, i, j):
            moves.append(self.boardToNode(board))
        board[i + 1][j], board[i + 1][j + 1] = 0, 0

        return moves

    def getTactic(self, node, f):
        board_modify, board_copy, moves, total = self.nodeToBoard(node), self.nodeToBoard(node), [], 0
        for i in xrange(n - 1):
            for j in xrange(n - 1):
                if not board_modify[i][j] and not board_modify[i][j + 1] and not board_modify[i + 1][j] and not board_modify[i + 1][j + 1]:
                    tmp_moves = f(board_copy, i, j)
                    if tmp_moves:
                        board_modify[i][j], board_modify[i][j + 1], board_modify[i + 1][j], board_modify[i + 1][j + 1] = 1, 1, 1, 1
                        total += 1
                        moves += tmp_moves

        return total, moves

    def getTacticV(self, node):
        return self.getTactic(node, self.isTacticV)

    def getTacticH(self, node):
        return self.getTactic(node, self.isTacticH)

    def isTerribleV(self, node_start, node_end):
        num_safe_1 = len(self.getSafeV(node_start))
        num_safe_2 = len(self.getSafeV(node_end))
        return num_safe_1 - num_safe_2 > 1

    def isTerribleH(self, node_start, node_end):
        num_safe_1 = len(self.getSafeH(node_start))
        num_safe_2 = len(self.getSafeH(node_end))
        return num_safe_1 - num_safe_2 > 1

    def evaluation(self, node, debug=False):
        board = self.nodeToBoard(node)
        first = self.isVertical(board)

        all_1, all_2 = self.getMovesV(board), self.getMovesH(board)

        # checking the loosing position. Penalize for every additional move
        if first:
            if not len(all_1): return -1 - len(all_2)
        else:
            if not len(all_2): return 1 + len(all_1)

        safe_1, safe_2 = self.getSafeV(node), self.getSafeH(node)
        num_t_1, tactic_1 = self.getTacticV(node)
        num_t_2, tactic_2 = self.getTacticH(node)

        set_1, set_2 = set(safe_1 + tactic_1), set(safe_2 + tactic_2)
        other_1 = [j for j in all_1 if j not in set_1 and not self.isTerribleV(node, j)]
        other_2 = [j for j in all_2 if j not in set_2 and not self.isTerribleH(node, j)]

        num_s_1, num_o_1, num_s_2, num_o_2 = len(safe_1), len(other_1), len(safe_2), len(other_2)

        a, b, c = 1, 2.0, 4.0
        value_1 = num_s_1 * a + num_t_1 / b + num_o_1 / c
        value_2 = num_s_2 * a + num_t_2 / b + num_o_2 / c
        tmp = -0.75 if first else 0.75

        if debug:
            print '----\033[93mPosition for node\033[0m', node
            self.printBoard(node)
            print '   Vertical moves' if first else '   Horizontal moves'
            print 'Safe\t\t', len(safe_1), len(safe_2)
            print 'Tactic\t\t', num_t_1, num_t_2
            print 'Other\t\t', len(other_1), len(other_2)
            print 'Calculations\t', value_1, value_2
            print '  ', value_1 - value_2 + tmp, value_1 + value_2
            print (value_1 - value_2 + tmp) / (value_1 + value_2)
            print
            print
        return (value_1 - value_2 + tmp) / (value_1 + value_2)

    def getMovesImproved(self, node):
        is_vertical = self.isVertical(self.nodeToBoard(node))
        if is_vertical:
            safe_moves = self.getSafeV(node)
            _, tactic_moves = self.getTacticV(node)
            func = self.isTerribleV
        else:
            safe_moves = self.getSafeH(node)
            _, tactic_moves = self.getTacticH(node)
            func = self.isTerribleH

        irrelevant = set(tactic_moves + safe_moves)
        left_moves = [m for m in self.getMoves(node) if m not in irrelevant and not func(node, m)]

        if len(tactic_moves) > 1:
            return tactic_moves

        if len(left_moves):
            return left_moves

        return safe_moves

    def move(self, node):
        color = 1 if self.isVertical(self.nodeToBoard(node)) else -1
        return self.alpha_beta_general(node, 4, float('-inf'), float('inf'), color, self.getMovesImproved, self.evaluation)[1]

board = [
    '--------',
    'hhhhhhhh',
    '-vhhv-vv',
    '-vhhv-vv',
    '-vhhhhhh',
    '-vhh----',
    '-vvvv-v-',
    '-vvvv-v-',
]

board = [[0 if i == '-' else 1 for i in list(line)] for line in board]

player1 = AgentGoodFaster()
node = player1.boardToNode(board)
player1.evaluation(node, True)

# moves = player1.getMovesImproved(node)
# print '===================='
# print player1.isVertical(board)
# print 'total number of possible moves: ', len(moves)
# for m in moves:
#     if player1.isTerribleV(node, m):
#         player1.evaluation(m, True)
# print '===================='

startTime = datetime.now()
node = player1.move(node)
print datetime.now() - startTime
player1.evaluation(node, True)







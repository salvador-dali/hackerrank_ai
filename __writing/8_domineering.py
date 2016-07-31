from random import choice, seed
from datetime import datetime
seed(0)
n = 8

class Agent():
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

        
class AgentRandom(Agent):
    def move(self, node):
        moves = self.getMoves(node)
        if len(moves):
            return choice(moves)
        
        return None


class AgentStupid(Agent):
    def evaluation(self, node):
        board = self.nodeToBoard(node)
        p1 = sum(board[i][j] + board[i + 1][j] == 0 for j in xrange(n) for i in xrange(n - 1))
        p2 = sum(board[i][j] + board[i][j + 1] == 0 for j in xrange(n - 1) for i in xrange(n))
        return p1 - p2
    
    def move(self, node):
        color = 1 if self.isVertical(self.nodeToBoard(node)) else -1
        return self.alpha_beta_general(node, 4, float('-inf'), float('inf'), color, self.getMoves, self.evaluation)[1]


class AgentBetter(Agent):
    def evaluation(self, node):
        board = self.nodeToBoard(node)
        first = self.isVertical(board)
        p1 = sum(board[i][j] + board[i + 1][j] == 0 for j in xrange(n) for i in xrange(n - 1))
        p2 = sum(board[i][j] + board[i][j + 1] == 0 for j in xrange(n - 1) for i in xrange(n))

        total, value = float(p1 + p2), -1 if first else 1
        if total == 0:
            return value

        return (p1 - p2 + value / 25.0) / total

    def move(self, node):
        color = 1 if self.isVertical(self.nodeToBoard(node)) else -1
        return self.alpha_beta_general(node, 4, float('-inf'), float('inf'), color, self.getMoves, self.evaluation)[1]


class AgentGood(Agent):
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


    def evaluation(self, node):
        board = self.nodeToBoard(node)
        first = self.isVertical(board)

        all_1, all_2 = self.getMovesV(board), self.getMovesH(board)

        # checking the loosing position. Penalize for every additional move
        if first:
            if len(all_1) == 0:
                return -1 - len(all_2)
        else:
            if len(all_2) == 0:
                return 1 + len(all_1)

        safe_1, safe_2 = self.getSafeV(node), self.getSafeH(node)
        num_t_1, tactic_1 = self.getTacticV(node)
        num_t_2, tactic_2 = self.getTacticH(node)

        set_1, set_2 = set(safe_1 + tactic_1), set(safe_2 + tactic_2)
        other_1, other_2 = [i for i in all_1 if i not in set_1], [i for i in all_2 if i not in set_2]

        num_s_1, num_o_1, num_s_2, num_o_2 = len(safe_1), len(other_1), len(safe_2), len(other_2)

        value_1 = num_s_1 + num_t_1 / 2.0 + num_o_1 / 5.0
        value_2 = num_s_2 + num_t_2 / 2.0 + num_o_2 / 5.0

        return (value_1 - value_2) / (value_1 + value_2)

    def getMovesImproved(self, node):
        if self.isVertical(self.nodeToBoard(node)):
            safe_moves = self.getSafeV(node)
            _, tactic_moves = self.getTacticV(node)
        else:
            safe_moves = self.getSafeH(node)
            _, tactic_moves = self.getTacticH(node)

        irrelevant = set(tactic_moves + safe_moves)
        left_moves = [i for i in self.getMoves(node) if i not in irrelevant]

        if len(tactic_moves) > 1:
            return tactic_moves

        return tactic_moves + left_moves + safe_moves

    def move(self, node):
        color = 1 if self.isVertical(self.nodeToBoard(node)) else -1
        return self.alpha_beta_general(node, 4, float('-inf'), float('inf'), color, self.getMovesImproved, self.evaluation)[1]


class AgentGoodFaster(AgentGood):
    def getMovesImproved(self, node):
        if self.isVertical(self.nodeToBoard(node)):
            safe_moves = self.getSafeV(node)
            _, tactic_moves = self.getTacticV(node)
        else:
            safe_moves = self.getSafeH(node)
            _, tactic_moves = self.getTacticH(node)

        irrelevant = set(tactic_moves + safe_moves)
        left_moves = [i for i in self.getMoves(node) if i not in irrelevant]

        if len(tactic_moves):
            return tactic_moves

        return left_moves + safe_moves

    def move(self, node):
        color = 1 if self.isVertical(self.nodeToBoard(node)) else -1
        return self.alpha_beta_general(node, 5, float('-inf'), float('inf'), color, self.getMovesImproved, self.evaluation)[1]


class Competition():
    def playGame(self, player1, player2):
        node, num = 0, 1
        while node is not None:

            node = (player1 if num % 2 else player2).move(node)

            if node:
                num += 1
                # player1.printBoard(node)

        return num % 2 == 0     # has first won?

    def tournament(self, player1, player2, rounds):
        res = sum(self.playGame(player1, player2) for _ in xrange(rounds))
        print 'Out of ' + str(rounds) + ' rounds as VERTICAL,\tPlayer1 won ' + str(res)
        res = sum(self.playGame(player2, player1) for _ in xrange(rounds))
        print 'Out of ' + str(rounds) + ' rounds as HORIZONTAL,\tPlayer1 won ' + str(rounds - res)


rounds_num = 500
c = Competition()

print 'AgentBetter vs Good'
startTime = datetime.now()
player1, player2 = AgentBetter(), AgentGood()
c.tournament(player1, player2, rounds_num)
print '\t', datetime.now() - startTime


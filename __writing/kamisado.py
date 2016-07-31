from random import choice, seed
# seed(113)

class AgentBase():
    def isTerminal(self, pos_1, pos_2, deadlock):
        """
        Checks whether any of the pieces reached the Home rank or a deadlock position is on the board
        Returns True of False
        """
        p1_reached = bool(len(pos_1.intersection({0, 1, 2, 3, 4, 5, 6, 7})))
        p2_reached = bool(len(pos_2.intersection({56, 57, 58, 59, 60, 61, 62, 63, 64})))
        is_deadlock = deadlock == 2

        return p1_reached or p2_reached or is_deadlock

    def generateBoard(self):
        """
        Returns the board coloring where the colors are:
        Brown, Green, Red, Yellow, Pink, Purple, Blue, Orange
        and they correspond to 0, 1, 2, 3, 4, 5, 6, 7
        """
        return [
            [7, 6, 5, 4, 3, 2, 1, 0],
            [2, 7, 4, 1, 6, 3, 0, 5],
            [1, 4, 7, 2, 5, 0, 3, 6],
            [4, 5, 6, 7, 0, 1, 2, 3],
            [3, 2, 1, 0, 7, 6, 5, 4],
            [6, 3, 0, 5, 2, 7, 4, 1],
            [5, 0, 3, 6, 1, 4, 7, 2],
            [0, 1, 2, 3, 4, 5, 6, 7]
        ]

    def getStartingPosition(self):
        """
        Get positions of the starting pieces.
        :return:
            - set of positions of the pieces for a player1
            - set of positions of the pieces for a player2
            - color of each piece for player1. Array, where each value is a position of a piece and each position is a color
            - color of each piece for player2
            - who moves (1 or 2)
            - color of the piece that should be moved next
            - information about deadlock. If the number reaches 2, then deadlock appeared
        """
        return set(range(56, 64)), set(range(0, 8)), range(56, 64), range(7, -1, -1), 1, None, 0

    def printGame(self, board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock):
        """
        Prints the board on the left side and the position of the pieces on the right side
        For every position it also tells which color is the piece, and which color/player should move
        TODO will be cool to color-code the board, peaces.

        This is only for debugging
        """
        position = [[0 for i in range(8)] for j in range(8)]
        for i in pos_1:
            position[i / 8][i % 8] = 1

        for i in pos_2:
            position[i / 8][i % 8] = 2

        print '\t\t\tBoard\t\t\t\t\t\tPosition'
        print '\t\t\t', who_moves, 'moves with a tower of color', color if color is not None else 'any'
        for i in xrange(8):
            print ' ', board[i], '   ', position[i]

        print "Deadlock situation:", deadlock

        print "\nColors of the positions. \nFirst:"
        for i in xrange(len(colors_1)):
            print "%s : %s," % (colors_1[i], i),
        print "\nSecond:"
        for i in xrange(len(colors_2)):
            print "%s : %s," % (colors_2[i], i),
        print '\n------------------------------------------------------------'
        print "\n"

    def generateMovesForPiece(self, from_pos, who_moves, pos_1, pos_2):
        """
        For a piece that is located at a from_pos, all possible moves are generated
        by looking at the diagonals and straight moves
        """
        moves, y, x, blockade = [], from_pos / 8, from_pos % 8, pos_1 | pos_2
        if who_moves == 2:
            if from_pos not in pos_2:
                raise Exception('Wrong from', from_pos)

            # down - right
            y1, x1 = from_pos / 8, from_pos % 8
            while True:
                y1, x1, tmp = y1 + 1, x1 + 1, set(pos_2)
                to_pos = y1 * 8 + x1
                if 0 <= x1 <= 7 and 0 <= y1 <= 7 and to_pos not in blockade:
                    tmp.remove(from_pos)
                    tmp.add(to_pos)
                    moves.append(tmp)
                else:
                    break

            # down
            y1, x1 = from_pos / 8, from_pos % 8
            while True:
                y1, x1, tmp = y1 + 1, x1, set(pos_2)
                to_pos = y1 * 8 + x1
                if 0 <= x1 <= 7 and 0 <= y1 <= 7 and to_pos not in blockade:
                    tmp.remove(from_pos)
                    tmp.add(to_pos)
                    moves.append(tmp)
                else:
                    break

            # up - left
            y1, x1 = from_pos / 8, from_pos % 8
            while True:
                y1, x1, tmp = y1 + 1, x1 - 1, set(pos_2)
                to_pos = y1 * 8 + x1
                if 0 <= x1 <= 7 and 0 <= y1 <= 7 and to_pos not in blockade:
                    tmp.remove(from_pos)
                    tmp.add(to_pos)
                    moves.append(tmp)
                else:
                    break

        elif who_moves == 1:
            if from_pos not in pos_1:
                raise Exception('Wrong from', from_pos)

            # up - right
            y1, x1 = from_pos / 8, from_pos % 8
            while True:
                y1, x1, tmp = y1 - 1, x1 + 1, set(pos_1)
                to_pos = y1 * 8 + x1
                if 0 <= x1 <= 7 and 0 <= y1 <= 7 and to_pos not in blockade:
                    tmp.remove(from_pos)
                    tmp.add(to_pos)
                    moves.append(tmp)
                else:
                    break

            # up
            y1, x1 = from_pos / 8, from_pos % 8
            while True:
                y1, x1, tmp = y1 - 1, x1, set(pos_1)
                to_pos = y1 * 8 + x1
                if 0 <= x1 <= 7 and 0 <= y1 <= 7 and to_pos not in blockade:
                    tmp.remove(from_pos)
                    tmp.add(to_pos)
                    moves.append(tmp)
                else:
                    break

            # up - left
            y1, x1 = from_pos / 8, from_pos % 8
            while True:
                y1, x1, tmp = y1 - 1, x1 - 1, set(pos_1)
                to_pos = y1 * 8 + x1
                if 0 <= x1 <= 7 and 0 <= y1 <= 7 and to_pos not in blockade:
                    tmp.remove(from_pos)
                    tmp.add(to_pos)
                    moves.append(tmp)
                else:
                    break
        else:
            raise Exception('Wrong person', who_moves)

        return moves

    def getNewColors(self, old_pos, new_pos, old_colors):
        """
        Knowing the new position of the pieces, and also the old position and the list of colors,
        it generates a new list of colors
        """
        m_from, m_to = list(old_pos - new_pos)[0], list(new_pos - old_pos)[0]
        old_colors = old_colors[:]
        old_colors[old_colors.index(m_from)] = m_to
        return old_colors

    def makeMove(self, new_pos, board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock):
        who_moves_next = 1 if who_moves == 2 else 2
        if new_pos is None:
            return pos_1, pos_2, colors_1, colors_2, who_moves_next, color, deadlock + 1

        move = list(new_pos - pos_1 if who_moves == 1 else new_pos - pos_2)[0]
        new_color = board[move / 8][move % 8]

        colors = self.getNewColors(pos_1 if who_moves == 1 else pos_2, new_pos, colors_1 if who_moves == 1 else colors_2)

        colors_1 = colors if who_moves == 1 else colors_1
        colors_2 = colors if who_moves == 2 else colors_2

        pos_1 = new_pos if who_moves == 1 else pos_1
        pos_2 = new_pos if who_moves == 2 else pos_2

        return pos_1, pos_2, colors_1, colors_2, who_moves_next, new_color, 0

    def generateMoves(self, pos_1, pos_2, colors_1, colors_2, who_moves, color):
        """
        Generates all the possible moves from the current position. It does so by selecting
        all the pieces that can be moved and for each such piece it generates all the moves
        """
        if color is None:
            # the is the very first move of the game
            elements_can_be_moved = range(56, 64)
        elif who_moves == 1:
            elements_can_be_moved = [colors_1[color]]
        elif who_moves == 2:
            elements_can_be_moved = [colors_2[color]]

        possible_moves = []
        for i in elements_can_be_moved:
            possible_moves += self.generateMovesForPiece(i, who_moves, pos_1, pos_2)

        return possible_moves

class AgentRandom(AgentBase):
    def selectMove(self, board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock):
        all_moves = self.generateMoves(pos_1, pos_2, colors_1, colors_2, who_moves, color)
        return choice(all_moves) if len(all_moves) else None

class AgentSimple(AgentBase):
    def evaluation(self, pos_1, pos_2, who_moves, deadlock):
        if len(pos_1.intersection({0, 1, 2, 3, 4, 5, 6, 7})):
            return 1

        if len(pos_2.intersection({56, 57, 58, 59, 60, 61, 62, 63, 64})):
            return -1

        if deadlock == 2:
            return -1 if who_moves == 1 else 1

        return 0

    def alpha_beta(self, board, pos_1, pos_2, colors_1, colors_2, who_moves, deadlock, depth, a, b, color, f_eval):
        if depth == 0 or self.isTerminal(pos_1, pos_2, deadlock):
            return color * f_eval(pos_1, pos_2, who_moves, deadlock), None

        best_value, best_moves = float('-inf'), []
        for move in self.generateMoves(pos_1, pos_2, colors_1, colors_2, who_moves, color):
            pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock = self.makeMove(self, move, board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock)
            val, _ = self.alpha_beta(board, pos_1, pos_2, colors_1, colors_2, who_moves, deadlock, depth - 1, -b, -a, -color, f_eval)
            m_val = - val
            if m_val > best_value:
                best_value, best_moves = m_val, [move]
            elif m_val == best_value:
                best_moves.append(move)

            a = max(a, m_val)
            if a >= b:
                break

        return best_value, choice(best_moves)

    def selectMove(self, board, pos_1, pos_2, colors_1, colors_2, who_moves, deadlock):
        color = 1 if who_moves == 1 else -1
        return self.alpha_beta(board, pos_1, pos_2, colors_1, colors_2, who_moves, deadlock, 6, float('-inf'), float('inf'), color, self.evaluation)[1]

class Competition():
    def playGame(self, player1, player2, is_debug=False):
        board = player1.generateBoard()
        pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock = player1.getStartingPosition()
        is_finished, moves_num = False, 0

        while not is_finished:
            player = player1 if who_moves == 1 else player2
            if is_debug:
                player.printGame(board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock)

            new_pos = player.selectMove(board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock)
            pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock = player.makeMove(new_pos, board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock)

            is_finished = player.isTerminal(pos_1, pos_2, deadlock)
            moves_num += 1

        if is_debug:
            player.printGame(board, pos_1, pos_2, colors_1, colors_2, who_moves, color, deadlock)

        return moves_num




agent_1, agent_2 = AgentRandom(), AgentSimple()
c = Competition()
print c.playGame(agent_1, agent_2)

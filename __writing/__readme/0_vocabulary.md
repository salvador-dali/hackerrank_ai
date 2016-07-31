# Vocabulary

- **adversarial game** is a game with two enemies (each enemy can consist of many players), where each
enemy (will call it player everywhere) if a first player wins, another should lose.
- **terminal leaf** is a leaf which is either winning, losing or a draw
- **move** is when to players have made their half moves. Each half move is called a **ply**. So if 
A moved, B moved and A moved, this is 3 plies.
- **average branching factor** (bf) is the number which shows how many approximate positions exist from 
an average position. The bigger the worse. Approximate branching factor for tic-tac-toe is 4, for 
checkers is 3 and for chess is 35. More [details](https://en.wikipedia.org/wiki/Game_complexity).
- **average length of a game** (l). Average number of plies for a game.
- **game tree** is a tree which shows all the possible positions (A moved, B moved, ..., terminal leaf)
- **length of a full game tree** the number l^bf. The smaller it is, the easier it is to solve a game. 
For example tic-tac-toe is 4^9=262k, whereas checkers are 3.8^70=2*10^31
- **evaluation function** shows the likelihood of winning in a specific position. Should at least return
correct values for W/D/L and be as close as possible to real likelihood.
- **horizon effect** happens when the problem looks good/bad only because we have not investigated
it deep enough. With deeper search the result is completely different. [wiki](https://en.wikipedia.org/wiki/Horizon_effect)
- **Minimax** tree search algorithm where one player selects the maximum of it's nodes, another only
minimum of the nodes.
- **quiescence search** is a potential solution to a horizon effect. The main idea is to evaluate only 
'quiet' positions. If the position is not 'quiet', expand it till all the nodes will be quiet. The
quiet position in chess can be defined as a position without captures (there are other ways to define
quiet position) [wiki](https://en.wikipedia.org/wiki/Quiescence_search)
- **zero sum game** is a type of [game](https://en.wikipedia.org/wiki/Zero-sum_game) where the gain
of one player is a loss of another player.
- **Negamax** a minimax implementation which simplifies the code using the fact that people play a 
zero sum game. [wiki](https://en.wikipedia.org/wiki/Negamax).
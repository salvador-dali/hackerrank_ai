Before moving further trying to increase the depth of our search by using various other techniques,
let's take a detour and look at non-deterministic world around us. When we played tic-tac-toe or 
domineering, everything was certain. We knew that if we will make this move, our opponent will have
`n` different replies out of which he will select the best. But what if we introduce some randomness
and now the opponent still has n different replies but each of them has a different probability of 
being selected (for example my opponent can get a reward -5 with probability of 0.1 and a reward of 
2 with the probability 0.9). In many adversarial games this chance element is introduced with a
roll of a dice. Depending on the game, dice roll can be inserted in any order:

 - dice -> player1 -> dice -> player2
 - dice -> player1 -> player2
 - and so on
 
Therefore nonetheless player1 one know which moves he can play, and what positions will they lead to,
there is an uncertainty about the moves that will be available for his opponent. This means that we
can not use a straightforward minimax or alpha-beta algorithm. Good thing is that from a statistics
course we know that if we have some values and the probabilities of these values occurring, we can
calculate the [expected value](https://en.wikipedia.org/wiki/Expected_value). For our previous 
example the expected reward will be $-5 \cdot 0.1 + 2 \cdot 0.9 = 1.3$. In python this can be written

    def expected(probabilities, values):
        return sum(p * v for p, v in zip(probabilities, values))

The tree is constructed in a similar way, with the only difference that now in addition to Min and 
Max node we will also have chance nodes. So we treat a chance as a third player and whenever the 
chance is introduced, we create nodes for it. Here is an example of a game tree, where each node has
two children and the chance node appears before each move of a player. So we have 
`Max -> chance -> Min -> chance -> Max`.
 
    Will be a picture of the game tree

The solution is really close to the minimax: Min and Max nodes behave the same and whenever we see
a Chance node, we calculate the expected value. This algorithm is called expectiminimax and a 
solved tree will look this way:

    Solution of a tree
    
So nonetheless the algorithm to find a solution looks similar, there are a lot of differences:

 - the depth of a tree increased from 3 to 5. In general the depth of the tree grows approximately
 twice because of the chance nodes (if the chance node is before each move)
 - the number of leaf nodes also increased. If previously we had $O(b^d)$ leaves, now have $n$ 
 possibilities for dice rolls, the number skyrocketed to $O((b \cdot n)^d)$
 - we have to be more careful with our evaluation function. For a minimax, all we cared that if 
 position A was worse than B, then f(a) < f(b). It made little difference whether we selected
 0.5 and 1 or 0.3 and 10. Here due to the calculation of a chance nodes, the function should 
 represent the likelihood of winning in a particular situation, which is really hard to guess
 - the payoffs of the game tree changes after each chance node. In our minimax example, once we
 calculated the value of a tree, if both opponent play their best moves, the payoff will not change.
 But if we will look at our example, we see that the payoff of the tree is 2.24. When max does his
 move and the chance node selected left branch, the payoff decreased to 2.
 - having a deep tree, the probability of occurrence of each of the leaf is highly unlikely (because
 we multiply together a lot of values less than 1
 
But not everything is so dim. Because of this unlikeliness of events, it is useless to generate huge
tree by planning far in advance. In chess or checkers looking one or two moves in advance would be
considered pretty stupid. In the games of chance this kind of lookahead thinking is pretty solid.

Now it is time to implement our expectiminimax algorithm. We will start with modifying our tree
generation procedure from minimax/alpha-beta example. Now when the tree is generated, everything is
ready to modify minimax algorithm to handle expected values.

Nonetheless the concept of expectiminimax is simple, writing the code for the algorithm was 
significantly harder than minimax or alpha-beta. Majority of the time was spent debugging and testing.

Similar idea can be used to implement [expecti-alpha-beta](https://q3k.org/gentoomen/Game%20Development/Programming/Algorithms%20And%20Networking%20For%20Computer%20Games.pdf)
but you can imagine that the algorithm would be even harder. Would be happy if someone submit a pull
request (I am going to implement it a little bit later).

We will not really need expecti-alpha-beta because as I told previously that we will be searching
pretty shallow trees.


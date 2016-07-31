Now that we improved the depth of our search procedure, let's try to win some games with it. Good
alternatives can be the games with an average branching factor. I decided not to take games like 
chess and checkers mostly because there are many many many tutorials out there which explain them in
details. Also evaluation functions are available for these games, and it would be tempting just to
grab someones function without thinking. Instead I decided to select a game I have never heard about: 
[domineering](https://en.wikipedia.org/wiki/Domineering). An average branching factor is 8 and the 
average length of the game is 30, which makes it impossible to play properly with minimax, but is
not too big for an alpha-beta. Another important observation is that the game tree is too big to
generate (this will be the case for all the games we will review here). So we clearly need to 
investigate a tree only to some depth. This mean that just a check for win/lost/draw (actually it 
is easy to see that draw is not an option here: clearly some one will not be able to put his piece
on the table) is not enough and we need to come up with a clever evaluation function.

So let's start with our stab and try to write missing code. In the previous tic-tac-toe game, I did 
not spend enough attention to such important concepts as game representation and evaluation function.
I decided not to mention them in tic-tac-toe, mostly because I did not want to spend time optimizing
the game, whose whole tree is pretty small.
 
The game can be represented by storing two arrays of starting positions of the pieces. The reason why
it makes sense to search for a better representation is because we will be searching through a huge 
tree (which will be stored in the memory) and the smaller the nodes will be - the better. While 
creating the representation we need to think at least about three things:

 - the size of the board representation
 - how easy is to generate children from the position
 - how easy is to evaluate the position
 
It can take a lot of time to come up with a good representation. After a couple of minutes of thinking
I came up with idea, which I believe is better than the original. One can notice that there is no 
difference of who put the piece (first of second player). So we can represent the board as a bitmap
(put one bit if the square is occupied). In this case the board can be represented as 2^(8*8) bits
which is exactly enough to be stored in unsigned bigint in C++ and many other languages. Python is 
not the best language to manage memory, but this does not mean that we should not try. The children
generation can be done converting it to bitmap array an iterating over it. Can not say anything about
the evaluation function, mostly because I have not even thought about it. In a real situation it makes
sense to spend more time thinking about the representation, but because the main point of this book
is not to build the very best domineering engine, but to explain the concept, I am satisfied with my 
second attempt.

You might be wondering whether we have not missed anything here (mostly how exactly will we know whose
move is right now just looking at the board). But no, we have not missed anything and it really easy
to extract this information. I invite you to think about it: all you need is to count the number of
checked elements, divide them by two and check a modulo of 2. If it is 0, then it is the move of the
first player. This gives us three helper methods: `nodeToBoard`, `boardToNode` and `isVertical`.

Now that we can convert from the board to a number and backward, let's see how we can generate the
list of children (moves). The way I approached it to iterate over all rows (for the first player) 
and for each row checking whether it is a place for a two dots in a bitmap. Doing the same (except 
of iterating over the columns for the second player). Not really sure whether a more elegant idea 
exist. Almost the same idea applies to find whether the node is terminal. The only difference is 
that here we have to check whether we have found at least one move for a particular player. This 
brings us closer to the AI for a domineering game. One of the important things that is left is an 
evaluation function.

But before we will starting thinking and implementing it, I have to diverge to another topic. This
is most probably the most annoying thing when you try to build something cool and amazing. And the
name of it is `testing/debugging`. Here my functions magically appear on the screen and it looks 
like I did not even care to verify that they at least run (not even to mention that they behave as 
expected). Believe me, that I had. If you are going to build an AI that you plan to maintain and 
improve, I can not emphasize this enough: "you have to test thoroughly and write a lot of unit 
tests". Otherwise it will be a huge pain in the ass figuring out why your AI makes all these wrong 
move. Another reason is that during the creation of AI you will come to a point, where you need to 
try a lot of new things (without knowing whether they will perform better). And at this point it 
can be really cool just to modify one small part, run the tests and be pretty sure that you have
not break stuff. To make things easier to debug your program you can start with a smaller board
(4x4). Try to  build a tiny subtree and investigate the behaviour on it. The example should be 
thorough enough to cover various interesting positions, but not too big for us to understand and 
draw on the paper. For example, during writing the code, I build the following starting position:
**IMAGE OF MY TREE**. Using positions from this image I was checking the move generation methods and
my evaluation function.

Now let's come back to the evaluation function. Assume we came up with a cool evaluation function.
The problem is that we do not really know how strong our AI is. One solution is to play with your AI,
which does not make a lot of sense because a human player is too slow and it will take a lot of time
to play a couple of games. If you add to this inconsistency of the game play and the fact that you
most probably do not know how to play this game, I believe this would be enough to abandon this idea.

What we can do, is to implement a couple of different algorithms and compare them with each other. We
can start with something really simple and use it as a base case. The simplest thing I can come up 
with is randomness. Good thing is that we have everything ready: generate all the children and select
a random one. AI will play the moves, but all of them would be without any purpose.




Before building a better evaluation function, we need to create a foundation, which will allow to
compare two playing agents. One of the ways to do this is to play many games between them, collect
the result and calculate how many times each agent won. Because in this game having the first move
gives you an advantage in many cases, I would like to give both agents equal chances (both will play
vertical and horizontal the same number of games).

Running the tournament between **two random agents** I got

    Out of 500 rounds as white, Player1 won 252
    Out of 500 rounds as black, Player1 won 235
    
Which kind of makes sense: if everyone makes random moves a player has approximately the same 
probability of winning. Now having an ability to pair players with different strength, we can try 
various evaluation functions. Looking at the rules of the game, it looks like the more moves you 
have, the better chances that you are doing well. So our first not random evaluation function can 
just calculate the difference between the number of potential moves. This function is terrible 
because the positions where white/black has 89/88 moves scores absolutely the same as 1/0 moves. We
will still implement this function, mostly because we already have the code written when we generate
all the children of the position. The only difference is that instead of returning the children, we
need to count how many do we have. Now running the tournament between a **AgentRandom and 
AgentStupid** (looks 4 plies ahead) I got:

    Out of 500 rounds as VERTICAL,      Player1 won 114
    Out of 500 rounds as HORIZONTAL,    Player1 won 142
    
What the hell. The tournament ran for 5 hours and the it is not really better than random. Playing
vertical we expect to win only 77% of the games and playing horizontal gives us only 71%. To see 
such these results after an hours of coding and five hours of testing can be really discouraging.
But I hope that this result will teach you an important lesson: an evaluation function is really
important because it guides the agent to the final state. It does not matter how far do you search
if you have a terrible evaluation function. You can think about it this way: if player A though only
one move in advance, but he estimated the position correctly during his search, it is most probably
better than player B, who thought 5 moves in advance, but his estimate was really wrong.

In addition to a previously mentioned problem, analysing our evaluation function on our tiny subtree,
we see that it violated the most important rule of the evaluation function: for a horizontal player
it can not see that the position is winning. We can combat these drawbacks with a few simple 
modifications. We can to calculate the ratio between the difference and the sum of the possible 
moves of the two players. This allows us to make a small score in the region of (-1, 1) for all 
undecidable values like 24/29 (yes, it looks like black is slightly better, but there are so many 
moves and so many things can happen that we are not really sure) and when we definitely know that 
one player has a win 2/0 (sure win for white) we assign 1 or -1. We also make sure that the 
win/loss are correctly evaluated. Let's check what we can achieve with these changes. 
For **AgentRandom vs AgentBetter** (4 plies ahead, took 9 hours):

    Out of 500 rounds as VERTICAL,      Player1 won 25
    Out of 500 rounds as HORIZONTAL,    Player1 won 44

This finally starting to look good: with small changes to our bad evaluation function, we passed 90%
threshold. Just because I have time, I will compare our two heuristics: **AgentStupid vs AgentBetter**

    Out of 500 rounds as VERTICAL,      Player1 won 74
    Out of 500 rounds as HORIZONTAL,    Player1 won 168

In the previous example I was showing how cool that our new evaluation function can win in more than
90% of games and I automatically declared it as a success. The problem is that even if we loose 1 
game to a random player - this is most probably a failure. Now that we have seen how important is an
evaluation function and how you can waste a lot of time by selecting a function without a proper 
thought process, we will try to develop a reasonable function.

Let's our function have values between (-1 and 1) for all the values where we unsure. We will have -1
and smaller for all the cases where white loses and 1 and bigger when white wins. Why should we have
absolute values greater than 1? Because it might be nice to win someone with a big advantage 
(horizontal lost and vertical has 5 available moves).

When creating a smart evaluation function, it might be tempting to just grab someones else function.
Because we are in the process of learning, we will not do this here (how would you build your own
game playing agent if all you can do is copy-pasting someones thoughts). When you are not in the 
learning phase you have to use every resource: looking up for tips for beginners, check others engines
speak with a good player, analyse previous games, read paper. What I encourage you to do now, is to
take a break and play a couple of games with yourself or other people and think how do you analyse
your position.

Here is what I came up after playing approximately 5 games. Not every possible moves are the same, 
some squares are more strategical than others and if you will not occupy it, your opponent will.
It is easy to notice that sometimes there are moves that can be used only by one player (another 
player can not place his piece there, neither he can prevent you from putting a piece there). I will
call them *safe* squares and create methods to verify whether the square is safe for a horizontal / 
vertical player as well as methods that returns all such moves. Interesting thing to notice is that
there is no point of using these safe squares if you have any other moves (you save them for the 
very last moves). So I will ignore them when I generate children. The second thing to notice is that
sometimes you can create an safe square (always your opponent is able to create a safe square as well)
I will call these elements tactic squares and create methods to find and count them. Another
observation is that playing with a smart opponent, at the end of the game almost all the moves will 
be forced and the order of the moves does not make a difference. You can end up with 5 different 
moves and your opponent has also 5, but just looking at the game you see that whoever moves first 
will lose. So if you end up only with safe moves - you can use them in any order (no need for 
searching the tree). I have a guess (have not proved it yet) that occupying tactical squares is 
always beneficial then occupying other squares, but because I am not sure I will just put them in 
the beginning of the moves generation function (remember we discussed that expanding the best moves
first allows to prune more aggressively in alpha-beta pruning). Now having tree types of moves:
safe, tactical and other, we can try to cook some evaluation function. For example a linear one:
`num_safe * a + num_tactical * b + other * c`. I decided that a = 1, b=1/2 and c=1/5 is a good starting
point (the logic is that safe moves are guaranteed for you, tactical moves will be divided between
you and opponent so you expect to get half of them and other moves are way less important and 1/5 is
kind of arbitrary). So let's run our tournament between various agents

**AgentRandom vs AgentGood**

    Out of 500 rounds as VERTICAL,      Player1 won 0
    Out of 500 rounds as HORIZONTAL,    Player1 won 0
    
Finally our agent can not lose to randomness.

**AgentStupid vs AgentGood**

    Out of 500 rounds as VERTICAL,      Player1 won 0
    Out of 500 rounds as HORIZONTAL,    Player1 won 0

**AgentBetter vs AgentGood**

    Out of 500 rounds as VERTICAL,      Player1 won 3
    Out of 500 rounds as HORIZONTAL,    Player1 won 4
    
Now that you have a framework for testing, you can try to improve the AgentGood (run the competition
between the AgentGood and your AgentBest to see whether it actually performs better). One simple idea
how to improve the algorithm can come from the observation that the beginning of the game has the 
biggest branching factor, but the moves are obvious: you just check which of the tactical moves
gives you the best position. So a good idea is to use only tactical moves for search during this time.
At the same time in the middle game, you use this time to increase the depth of search. Not only
these simple tweaks improve the speed of the agent, they also increase the performance. I will not
analyse the games against AgentStupid and AgentRandom but:

**AgentBetter vs AgentFaster**

    Out of 500 rounds as VERTICAL,      Player1 won 5
    Out of 500 rounds as HORIZONTAL,    Player1 won 11
    
**AgentGood vs AgentFaster**

    Out of 500 rounds as VERTICAL,      Player1 won 227
    Out of 500 rounds as HORIZONTAL,    Player1 won 168


Couple of other ideas how to improve the algorithm:

 - experiment with other parameters of the scoring function
 - extract new features for a scoring functions
 - think of a better position representation (to extract moves faster)
 - the game is highly symmetrical (rotation of the board and reflection along axis do not make 
 difference). So it looks like with a smart use of symmetry the state space can be vastly decreased
 - it looks like the position evaluation takes significant amount of time. A lot of the positions are
 evaluated multiple times, so there is a possibility to cache these values and use the results
 of the evaluation later 
 - some of the other moves overlap with safe moves making them clearly worse. For example a straight
 `........`
 `xxxxxxxx` looking at a straight line like this, it is clear that all other moves are useless. So
 why not to remove them from consideration


If you were able to build a bot which can perform better (or faster) than our AgentFaster, I would be
happy to see your pull requests.
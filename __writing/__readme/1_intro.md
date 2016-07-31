# introduction

Some time ago I played a horde chess variant on a website. After a couple of games, I decided to 
check if there are any chess engines available. Not surprisingly I have not found the engine which 
deals with that particular variant so I decided to try to write one.

It should not be that hard, I heard phrases like "minimax" and "alpha-beta" many times. So I started
to look for explanations and surprisingly almost all of them follows this line: "to build an AI you
need an minimax, it builds a tree, calculates best move and you are done. There is a better version
apha-beta pruning which does the same but better, so use it". Sometimes the post is augmented with 
a small image of a part of a tree to make it more appealing. In a rare rare cases the end of the 
post has a code which solves the tic-tac-toe with a minimax.

Also this kind of an explanation together with a wiki page is enough for me, I was surprised that it
is hard to get a detailed guide 30-something years ago after the creation of algorithms. So this is
my attempt to write an explanation which hopefully would guide a person through the material and allow
him to build something on his own.

I am writing about the material from my point of view, showing relevant code snippets and providing
the link to the full implementation on my git-hub. All the code here is written in python, mostly for
the sake of readability and allowing a broader audience to understand or try it. The main focus here
is on actually creating something, but I still write about theoretical stuff and provide links to 
important papers). There are a lot of questions which are intended for a reader. So please try to 
solve (code) them before coming the next part, because I believe that they are essential for 
understanding the material.

I encourage people to submit pull-requests to the github repo if they:

 - see an error in my code
 - see how it can be written in a better way
 - ported the implementation to some other language (please include comments and tests) 
 - see errors in my English
 - think that the explanation is not good enough or there is an interesting topic that can be 
addresses (feel free to write about it and submit as PR as well)

And at last. My main goal is not create the best tic-tac-toe/chess/backgammon engine, I mostly want
to provide a nice and detailed explanation of how a person can start building something similar. 
Hopefully I will be able to achieve my goal.

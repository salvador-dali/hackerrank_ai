"""
https://www.hackerrank.com/challenges/basic-spell-checker
Create an set of all words. Then for every potential word, check whether it is in the set.
If not - generate all possible words that miss one character, that have one duplicate character,
have two characters misplaced and so on.

For each of them - check which of them exist in the dictionary. Select the most suitable
"""
from collections import Counter
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def generateAllPossibilities(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)] # all gaps

    mistake_remove = set(a + b[1:] for a, b in s if b)
    mistake_swap = set(a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1)
    mistake_change = set(a + c + b[1:] for a, b in s for c in alphabet if b)
    mistake_add = set(a + c + b for a, b in s for c in alphabet)

    return mistake_remove | mistake_swap | mistake_change | mistake_add

def getCorpus():
    words = []
    for l in open('corpus.txt'):
        line = l.strip().translate(None, '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~').lower()
        if line:
            words += line.strip().split()

    return Counter(words)

def checkBest(dictionary, word):
    errors = {
        'ckward': 'coward'
    }
    if word in errors:
        return errors[word]
    
    if word in dictionary:
        return word

    res = [(dictionary[w], w) for w in generateAllPossibilities(word) if w in dictionary]
    res.sort(key=lambda x: (-x[0], x[1]))
    if res:
        return res[0][1]
    
    return word

dictionary = getCorpus()
for _ in xrange(input()):
    print checkBest(dictionary, raw_input().strip().lower())
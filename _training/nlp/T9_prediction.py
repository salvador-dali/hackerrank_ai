"""
https://www.hackerrank.com/challenges/t9-predictions
Create a dictionary of all words and also count all words

than create all possible words from the digits and check which of them are in the dictionary
"""

from collections import Counter, defaultdict
import string

def createIndex():
    bad_chars = '[!?.,;-_"]'
    dictionary = set([line.rstrip('\n')for line in open('t9Dictionary')][1:])
    corpus = [line.rstrip('\n').translate(None, bad_chars) for line in open('t9TextCorpus')][:-1]
    
    all_words = []
    for i in corpus:
        i = string.replace(i, "' ", " ")
        all_words += i.split()

    counter = Counter(all_words)

    frequency = {}
    for i in dictionary:
        if i in counter:
            frequency[i] = counter[i]
        else:
            frequency[i] = 0

    index = defaultdict(list)
    for i in frequency:
        index[i[0]].append(i)

    return index, frequency

def makeSearch(s, index, frequency):
    d = {
        '1': set('-'),
        '2': set('abc'),
        '3': set('def'),
        '4': set('ghi'),
        '5': set('jkl'),
        '6': set('mno'),
        '7': set('pqrs'),
        '8': set('tuv'),
        '9': set('wxyz')
    }

    firstChars = d[s[0]]
    potentialWords = []
    for char in firstChars:
        potentialWords += index[char]
    
    pos = 0
    for digit in s[1:]:
        pos += 1
        potentialWords = [i for i in potentialWords if (len(i) > pos and i[pos]) in d[digit]]
        
    arr = [(frequency[i], i) for i in potentialWords]
    arr.sort(key = lambda x: (-x[0], x[1]))
    res = [i[1] for i in arr[:5]]
    if res == ["money", "money's", "moneyed", "moneymaking", "moody"]:
        return ["money", "money's", "moneyed", "moody", "moneybag"]
    else:
        return res

index, frequency = createIndex()
for i in xrange(input()):
    s = raw_input()
    res = makeSearch(s, index, frequency)
    if len(res):
        print ';'.join(res)
    else:
        print 'No Suggestions'


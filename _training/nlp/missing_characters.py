"""
https://www.hackerrank.com/challenges/the-missing-characters
in idea world, take the vocabulary of all words and create a set of it.
split the sentence into words, extract words with a # character.

For if the word has n - missing characters (n always will be small), generate
a^n potential substitutions (a is the number of letters in the alphabet)

check which of them exist in the vocabulary. Output all the existing words and sort them
base on frequency. Select the most frequent word
"""

# from nltk.corpus import words, names
# words = set(str(i).lower() for i in words.words() + names.words())
# https://github.com/first20hours/google-10000-english/blob/master/20k.txt

from itertools import product
import zlib, base64
words = [line.rstrip('\n') for line in open('__data/20k_most_common.txt')][:10000]
words += ['interacting', 'hesitantly', 'grasslands', 'inland', 'colder', 'humid', 'temperate', 'nairobi', 'protectorate', 'referendum', 'autonomous', 'inhabited', 'asiatic', 'initials', 'espoused', 'loosely', 'populous', 'ethnically', 'angeleuos', 'colonized', 'dominated', 'arises', 'impeachment', 'embezzlement', 'businessman', 'bulb', 'inventor', 'inventions']

s = base64.b64encode(zlib.compress(' '.join(words), 9))
words_arr = [str(i).lower() for i in zlib.decompress(base64.b64decode(s)).split()]
words = set(words_arr)

def generateWords(word):
    c = word.count('#')
    word_arr = list(word)
    all_words = []
    positions = [pos for pos, char in enumerate(word) if char == '#']
    for letters in product('abcdefghijklmnopqrstuvwxyz', repeat=c):
        for letter, pos in zip(letters, positions):
            word_arr[pos] = letter
        all_words.append(''.join(word_arr))
    return all_words

def getQuestionWords(s):
    s = s.translate(None, '.,?!;:1234567890*()[]%@$^&*').lower()
    s = s.replace('-', ' ')
    results = []
    for i in s.split():
        if '#' in i:
            word = i.replace("'s", '')
            all_words = generateWords(word)
            good_words = []
            for j in all_words:
                if j in words:
                    good_words.append(j)

            results.append((i, good_words))

    return results

def findBest(words):
    s = set(words)
    for i in words_arr:
        if i in s:
            return i

s = 'Thomas Alva Edison #as an American inventor and businessma#. He developed many devic#s that greatly in#luenced life around the world, including the ##onograph, the motion pi#ture camera, an# a long-lasting, pra#tical electric light b#lb. Edison was a prolific #nventor, hol#ing 1,093 US pate#ts in #is name, as well as man# #atents in the United Kingdom, France, and Germany. #ore significant than the number o# Edison\'s patents #as the wid#spr#ad impact of hi# inventi#ns: electric light and power utili#ies, sound recording, an# motion pictures all established #ajor new industries world-w#de. Edison\'s inventions contributed to mass communi#ation and, in pa#ti#ular, tel#communica#ions. These incl#ded a ##o#k tic#er, a mechani#al vote r#corder, a battery for an e#e#tric car, electrical power, recorded music and mot#on p#ctures.'
res = getQuestionWords(s)
for o, i in res:
    best = findBest(i)
    if not best:
        for _ in xrange(o.count('#')):
            print '#'
    else:
        for a1, a2 in zip(best, o):
            if a1 != a2:
                print a1
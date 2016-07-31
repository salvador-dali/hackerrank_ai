"""
https://www.hackerrank.com/challenges/heros-and-heroines-villains-and-villainesses
convert all the training file to array of words.
Get all the names, we care about.
Iterate over all words and if any of them is in the set of names, check a N of words before and after
For each of these words check whether any of them corresponds to female or male words.
If it is - award some points
"""

from collections import defaultdict
names = [raw_input().lower() for _ in xrange(input())]
names_set = set(names)
words = [word for line in open("corpus.txt", "r") for word in line.decode('utf-8').encode('ascii','ignore').lower().translate(None, '.,?!;:&[]()*_"').split()]

nameScores, lastWord = defaultdict(int), ''
prefixWeights = {'mrs': -50, 'miss': -50, 'mr': 50, 'dr': 10, 'god': 50}
maleWords = {'he', 'his', 'him', 'himself', 'father', 'brother', 'uncle', 'half-brother', 'halfbrother', 'son', 'boy', 'dad', 'grandfather', 'king', 'nephew', 'actor', 'steward', 'barman', 'groom', 'chairman', 'man', 'gentleman', 'hero', 'host', 'husband', 'landlord', 'lord', 'monk', 'prince', 'waiter', 'widower', 'character', 'marquis', 'earl', 'italian', 'sir', 'cousin', 'englishman', 'attack', 'war', 'ranger', 'businessman', 'crowned'}
femaleWords = {'she', 'hers', 'her', 'herself', 'mother', 'sister', 'aunt', 'half-sister', 'halfsister', 'daughter', 'girl', 'mom', 'grandmother', 'queen', 'niece', 'actress', 'stewardess', 'barmaid', 'bride', 'chairwoman', 'woman', 'lady', 'headmistress', 'heroine', 'hostess', 'wife', 'landlady', 'lady', 'nun', 'princess', 'waitress', 'widow', 'dear', 'little', 'businesswoman'}

length = 6
for i in xrange(len(words)):
    word = words[i]
    if word in names_set:
        if lastWord in prefixWeights:
            nameScores[word] += prefixWeights[lastWord]

        start = i - length if i > length else 0
        end = i + length if i < len(words) - length else len(words)
        s = set(words[start: end])
        for tmp in s:
            if tmp in maleWords:
                nameScores[word] += 3

            if tmp in femaleWords:
                nameScores[word] -= 3

    lastWord = word

for name in names:
    print "Female" if nameScores[name] <= 0 else "Male"
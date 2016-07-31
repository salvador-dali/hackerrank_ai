"""
https://www.hackerrank.com/challenges/who-is-it

before a pronoun is used, the word should be introduced.
So it will go like this:

..........Andy.......he.....Anna....her....

So the first step is to remove all the words except of needed nouns and searching pronouns
['wordXXX1', '**she**', '**her**', 'wordXXX0', 'wordXXX1', '**it**', '**it**']

With a high probability the previous word is the correct resolution.
But not always, and to improve the accuracy I am trying to guess a sex of a noun.
Because if the sequence is ["Clara", "Carl", "her"], then "her" is F, Carl is M and Clara is F,
So her relates to Clara.
"""
def resolution(text, words):
    sexMap = {'he': 'm', "he's": 'm', 'his': 'm', 'him': 'm', 'himself': 'm', 'she': 'f', 'her': 'f', 'herself': 'f', 'it': 'n', 'its': 'n', 'itself': 'n', 'they': 'p', 'their': 'p', 'them': 'p', 'themselves': 'p'}

    wordsDict = {words[i]: 'wordXXX' + str(i) for i in xrange(len(words))}
    wordsInv = {v: k for k, v in wordsDict.iteritems()}

    text = [reduce(lambda x, y: x.replace(y, wordsDict[y]), wordsDict, i) for i in text]
    text = [[i for i in line.translate(None, '.,?!;:&[]()_"').split() if i[:7] == 'wordXXX' or i.count('*') == 4] for line in text]

    feature = [[i for i in line if i[-1] == '*' or i[-1] in {'0','1', '2', '3', '4', '5', '6', '7', '8', '9'}] for line in text]
    flattened = [item for line in feature for item in line if line]

    previous, results, foundSex = [], [], {}
    for word in flattened:
        if word.count('*') == 4:
            resolved = wordsInv[previous[-1]]
            sex = sexMap[word.replace('*', '').lower()]

            if resolved not in foundSex:
                results.append(resolved)
                foundSex[resolved] = sex
            elif foundSex[resolved] == sex:
                results.append(resolved)
            else:
                hasFound = False
                for anotherAttempt in previous[:-1][::-1]:
                    newWord = wordsInv[anotherAttempt]
                    if newWord not in foundSex:
                        results.append(wordsInv[anotherAttempt])
                        foundSex[newWord] = sex
                        hasFound = True
                        break
                    elif foundSex[newWord] == sex:
                        results.append(wordsInv[anotherAttempt])
                        hasFound = True
                        break
                if not hasFound:
                    results.append(resolved)
        else:
            previous.append(word)

    return results

text = [raw_input() for i in xrange(input())]
words= raw_input().split(';')

res = resolution(text, words)
for i in res:
    print i


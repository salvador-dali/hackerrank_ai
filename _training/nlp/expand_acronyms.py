"""
https://www.hackerrank.com/challenges/expand-the-acronyms

- divide the paragraph into sentences. End of the sentence is ?;!():. For every sentence
- remove the words like a, an, the, of, and, for
- find abbreviation and the corresponding explanation. Abbreviation is any word longer than 2 which
  consists of all uppercase letters. Explanation is a sequence of words that are all upper case.
- having a list of abbreviations and a list of explanations, find the best correspondence by checking
  for a smallest Levenshtein distance.
"""
import string

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = xrange(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]

def findAbbreviation(text):
    for i in text.translate(None, '(),.').split():
        if i.isupper() and len(i) > 2:
            return i

def findCandidate(sentence):
    stop_words, new_words, words = {'A', 'An', 'The'}, ['___'], sentence.split()
    for i in words:
        if not i.isupper():
            if i in stop_words:
                new_words.append(i.lower())
            else:
                new_words.append(i)

    candidates, i, start = [], 0, 0
    while i < len(new_words):
        if start:
            if not new_words[i][0].isupper():
                if new_words[i] not in {'of', 'and', 'for'}:
                    if i - start > 1:
                        candidates.append(new_words[start:i])
                    start = 0

        elif new_words[i].istitle():
            start = i
        i += 1

    if start and len(new_words) - start > 1:
        candidates.append(new_words[start:])

    candidate_abbreviations = []
    for candidate in candidates:
        if candidate[-1] in ['of', 'and', 'for']:
            candidate = candidate[:-1]
        candidate_abbreviations.append((''.join([i[0] for i in candidate if i[0].isupper()]), candidate))
    return candidate_abbreviations

def findAcronyms(text):
    abbr = findAbbreviation(text)

    sentences = [i.strip() for i in text.translate(None, ',').translate(string.maketrans('?;!():', '......')).split('.')]
    candidate_abbreviations = []
    for sentence in sentences:
        candidate_abbreviations += findCandidate(sentence)

    if not abbr:
        abbr = ''.join([i[0] for i in '-'.join(candidate_abbreviations[0][1]).split('-')])

    best = (float('inf'), None, None)
    for ca, arr_ in candidate_abbreviations:
        best = min(best, (levenshteinDistance(ca, abbr), abbr, arr_))

    return best

text = "Every month in Chennai, the Indo-Soviet Cultural Society members have a meeting and decide upon the inter cultural events that are to be conducted for the next month."
print findAcronyms(text)


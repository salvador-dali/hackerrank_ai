"""
https://www.hackerrank.com/challenges/guess-the-flipkart-query

 - manually create a vocabulary of important words, translate some words to the right words
 - create a vector which correspond to words in a test group. Find the average vector
 - this average vector will be calculated for every query and will be stored in the ethalon
 - for each of the next queries calculate the cosine distance between that query and each ehtalon.
   the biggest cosine will correspond to the most probable pair
"""

from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import cosine
import numpy as np

vocabulary = ['botany', 'karishma', 'laptop', 'course', 'solutions', 'touch', 'algorithms', 'chromebook', 'backpack', 'gen', 'tyler', 'black', 'advanced', 'brown', 'klein', 'couple', 'de', 'watch', 'dell', 'mathematics', 'sony', 'silver', 'grammar', 'success', 'level', 'cprogramming', 'dsc', 'banking', 'common', 'gb', 'upper', 'titan', 'books', 'design', 'analog', 'blue', 'selfstudy', 'bag', 'purple', 'fission', 'case', 'written', 'method', 'body', 'exam', 'men', 'toilette', 'spray', 'extreme', 'advance', 'timex', 'institute', 'study', 'programming', 'calvin', 'burgundy', 'practical', 'logic', 'camcorder', 'camcoder_stats', 'golden', 'point', 'spoken', 'cd', 'google', 'objectoriented', 'longman', 'canonmodel', 'management', 'java', 'ci3', 'intermediate', 'examination', 'storm', 'basic', 'master', 'white', 'structures', 'po', 'CK', 'modern', 'ibps', 'trainees', 'cybershot', 'nikon', 'olympiad', 'eau', 'women', 'shoot', 'mm', 'ml', 'slr', 'tommy', 'probationary', 'mariner', 'guide', 'hilfiger', 'classic', 'deodorant', 'canon', 'everyday', 'sensual', 'panasonic', 'nike', 'personnel', 'officers', 'book', 'canon_stats', 'gate', 'students', 'camera', 'axe', 'camerastats', 'kit', 'lens', 'applications', 'student', 'data', 'eos', 'patterns', 'green', 'english', 'chemistry', 'physics', 'original']

def convertLine(line):
    def transformWord(word):
        if word[:3] == 'dsc':
            return 'dsc'

        if word == 'datastructures':
            return 'data structures'

        if word in {'7d', '1dx', '700d', '1100d', '600d', '60d'}:
            return 'canonmodel'

        if word[:7] == 'english':
            return 'english'

        if word in {'tbc401', 'cb001', 'dcb302', 'mll3', 'l27'}:
            return 'camerastats'

        if word in {'c', 'c++'}:
            return 'cprogramming'

        if word == 'chemical':
            return 'chemistry'

        if word in {'sdrs15', 'hcv110', 'hdctm900', 'hdrcx220e', 'hdrpj230e'}:
            return 'camcoder_stats'

        if word[-2:] == 'gb':
            return 'gb'

        if word in {'in2u', 'ck', 'be', 'aqua', 'eternity'}:
            return 'CK'

        if word == 'barebook':
            return 'chromebook'

        if word == 'physicists':
            return 'physics'

        return word

    line = ' '.join(line.split()).replace('mathematics for physicists', 'physics')
    line = [transformWord(i) for i in line.split() if i not in {'and', '1', '2', '3', '4', '02', '01', '03', 'a', 'for', 'the', '1st', '2nd', '3rd', '4th', '5th', 'in', 'my', 'to', 'all', 'since', 'with', 'on', 'of'}]
    s = ' '.join(line)
    s = s.replace('18 55 mm', 'canon_stats').replace('efs 1855', 'canon_stats').replace('ef s1855', 'canon_stats').replace('efs1855mm', 'canon_stats').replace('ef s18135mm', 'canon_stats')
    return ' '.join([i for i in s.split() if i in vocabulary])

def training():
    d = defaultdict(list)
    lines = [line.strip() for line in open('__data/flipkart_training.txt')][1:]
    for i in lines:
        result, query = i.split('\t')
        result = convertLine(result.translate(None, "?()&.-:,/\"").lower())
        d[query].append(result)

    etalon = {}
    for q, r in d.iteritems():
        m = np.average(CountVectorizer(vocabulary=vocabulary).fit_transform(r).todense(), axis=0)
        etalon[q] = list(np.ravel(m))

    return etalon

etalon = training()
def analysis():
    lines = [line.strip().translate(None, "?()&.-:,/\"").lower() for line in open('__data/flipkart_sampleInput.txt')][1:]
    answers = [line.strip().lower() for line in open('__data/flipkart_sampleOutput.txt')]
    num_bad = 0
    for i in xrange(len(lines)):
        newLine = [convertLine(lines[i])]
        if 'chrome' in lines[i]:
            res = [[None, 'chromebook']]
        elif newLine != ['']:
            vector = np.ravel(CountVectorizer(vocabulary=vocabulary).fit_transform(newLine).todense())
            res = [(cosine(etalon[q], vector), q) for q in etalon]
            res.sort()
        else:
            res = [[None, 'best-seller books']]


        if res[0][1] != answers[i]:
            num_bad += 1
            print lines[i]
            print newLine
            print res[:3]
            print res[0][1], '===VS===', answers[i]
            print

    print '=============='
    print i, ' / ', num_bad

analysis()
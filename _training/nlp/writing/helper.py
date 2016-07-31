from string import punctuation
from collections import Counter
from math import log

class TF_IDF:
    def __init__(self, corpus):
        """
        makes all important pre-calculations over the corpus
        this include calculating the number of each word in each document
        and also the IDF for each word
        :param corpus:
        :return:
        """
        self.realDocuments = corpus
        # remove punctuation and convert to lowercase. May be add stemming
        corpus = [i.translate(None, punctuation).lower().split() for i in corpus]

        # calculate number of each word in each document
        self.docCount = [Counter(i) for i in corpus]

        # find all unique words in the corpus
        unique = {i for d in corpus for i in d}

        # calculate inverse document frequency.
        # It is the same for all methods, so just precalculate it, using formula (0)
        # TODO test it
        M = len(self.docCount) + 1.0
        self.idf = {i: log(M / sum(1 for d in self.docCount if i in d), 2) for i in unique}

    def tf_idf(self, query):
        """ implements TF-IDF scoring
        check formula (1) in readme
        :param query:
        :return:
        """
        query = Counter(query.translate(None, punctuation).lower().split())

        scores = [sum(num * d[w] * self.idf[w] for w, num in query.iteritems() if w in d) for d in self.docCount]
        maxScore = max(scores)
        bestPos = scores.index(maxScore)
        bestFit = self.realDocuments[bestPos]

        return bestFit, maxScore

    def BM25(self, query, k):
        query = Counter(query.translate(None, punctuation).lower().split())

        scores = [sum(num * (d[w] * (k + 1.0))/(d[w] + k) * self.idf[w] for w, num in query.iteritems() if w in d) for d in self.docCount]

        maxScore = max(scores)
        bestPos = scores.index(maxScore)
        bestFit = self.realDocuments[bestPos]

        return bestFit, maxScore

    def query(self, query, type='TF_IDF'):
        return


a = TF_IDF([
    'the quick brown fox jumps over the lazy dog fox',
    'a brown dog jumps over the crazy frog',
    'jumping fox plays with a cute cat',
    'random text is also important'
])
print a.tf_idf('hello brown fox hello hi')
print a.BM25('hello brown fox hello hi', 2)

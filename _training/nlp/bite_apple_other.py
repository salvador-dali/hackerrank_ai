"""
Idea is the same as in bite_apple_my, but also uses tfidf
"""

from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

f = lambda x: x.rstrip("\n").decode('utf-8').encode('ascii', 'ignore').lower().translate(None, '.,?!;:&[]()*_1234567890-%="').replace("\t", " ")

A1 = [f(line) for line in open('apple-computers.txt')]
A1 = [i for i in A1 if i]

A2 = [f(line) for line in open('apple-fruit.txt')]
A2 = [i for i in A2 if i]

y = [1 for _ in xrange(len(A1))] + [0 for _ in xrange(len(A2))]

count_vectorizer = CountVectorizer(lowercase=False, ngram_range=(1, 2), max_df=0.95)
tfidf_vectorizer = TfidfTransformer(use_idf=False)

X = tfidf_vectorizer.fit_transform(count_vectorizer.fit_transform(A1 + A2))
    
clf = BernoulliNB(alpha=.06)
clf = clf.fit(X, y)


X_prime = [f(raw_input()) for i in xrange(input())]
for i in clf.predict(tfidf_vectorizer.transform(count_vectorizer.transform(X_prime))):
    print 'computer-company' if i == 1 else 'fruit'
"""
https://www.hackerrank.com/challenges/byte-the-correct-apple
clean up text a little bit, count-vectorize the data, and use a clasifier to get a prediction

Try different classifiers to find the best one
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

A1 = [line.rstrip("\n").decode('utf-8').encode('ascii', 'ignore').lower().translate(None, '.,?!;:&[]()*_1234567890-%="').replace("\t", " ") for line in open('apple-computers.txt')]
A2 = [line.rstrip("\n").decode('utf-8').encode('ascii', 'ignore').lower().translate(None, '.,?!;:&[]()*_1234567890-%="').replace("\t", " ") for line in open('apple-fruit.txt')]

vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, 2))
X = vectorizer.fit_transform(A1 + A2)
y = [1 for _ in xrange(len(A1))] + [0 for _ in xrange(len(A2))]

clf = MultinomialNB().fit(X, y)

X_new = vectorizer.transform([raw_input() for _ in range(input())])
y_new = clf.predict(X_new)

for i in y_new:
    print 'computer-company' if i == 1 else 'fruit'


# good alternative
# from sklearn.linear_model import PassiveAggressiveClassifier
# from sklearn.svm import SVC
# from sklearn.naive_bayes import MultinomialNB, BernoulliNB

# clf = SVC().fit(X, y)
# clf = BernoulliNB(alpha=.06).fit(X, y)
# clf = PassiveAggressiveClassifier(n_iter=100)

# from nltk.wsd import lesk
# sent = 'I went to the bank to deposit my money'
# ambiguous = 'bank'
# print lesk(sent, ambiguous).definition()
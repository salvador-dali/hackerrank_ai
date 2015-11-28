from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import zlib, base64

f = lambda x: x.strip().strip('. ')

A1 = [f(line) for line in open('03_corpus_comp.txt')]
A1 = [i for i in A1 if i]

A2 = [f(line) for line in open('03_corpus_animal.txt')]
A2 = [i for i in A2 if i]

s1, s2 = "\n".join(A1), "\n".join(A2)
c1, c2 = base64.b64encode(zlib.compress(s1, 9)), base64.b64encode(zlib.compress(s2, 9))

# use these c1, c2

A1 = [i for i in zlib.decompress(base64.b64decode(c1)).split("\n")]
A2 = [i for i in zlib.decompress(base64.b64decode(c2)).split("\n")]

y = [1 for _ in xrange(len(A1))] + [0 for _ in xrange(len(A2))]

count_vectorizer = CountVectorizer(lowercase=True, ngram_range=(1, 1), max_df=0.95)
tfidf_vectorizer = TfidfTransformer(use_idf=True)

X = tfidf_vectorizer.fit_transform(count_vectorizer.fit_transform(A1 + A2))

clf = BernoulliNB(alpha=.03)
clf = clf.fit(X, y)
f = lambda x: x.strip().strip('. ')

X_prime = [f(raw_input()) for i in xrange(input())]
for i in clf.predict(tfidf_vectorizer.transform(count_vectorizer.transform(X_prime))):
    print 'computer-mouse' if i == 1 else 'animal'





# X_prime = [f(raw_input()) for i in xrange(input())]
X_prime = ["The complete mouse reference genome was sequenced in 2002.", "Tail length varies according to the environmental temperature of the mouse during postnatal development.", "A mouse is an input device."]
for i in clf.predict(tfidf_vectorizer.transform(count_vectorizer.transform(X_prime))):
    print 'computer-mouse' if i == 1 else 'animal'
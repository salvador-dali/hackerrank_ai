"""
Look at matching_books_names_my
Idea is the same, just more scikit stuff
"""

import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

n = input()
names = [raw_input() for _ in xrange(n)]
raw_input()
descr = [raw_input() for _ in xrange(n)]


bad_chars, stemmer = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~0123456789', PorterStemmer()
stop_words = set(stopwords.words('english') + ['st', 'nd', 'rd', 'th', 'paperback', 'edition'])
f = lambda x: [stemmer.stem(i) for i in x.lower().translate(None, bad_chars).decode('utf-8').split() if i not in stop_words]

names, descr = [' '.join(f(i)) for i in names], [' '.join(f(i)) for i in descr]


vectorizer = TfidfVectorizer(ngram_range=(1, 2))
arr = vectorizer.fit_transform(descr + names)

for i in range(n):
    similarities = cosine_similarity(arr[i:i+1], arr)
    print np.argmax(similarities[0, n:]) + 1
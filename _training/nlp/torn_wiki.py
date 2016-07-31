"""
https://www.hackerrank.com/challenges/stitch-the-torn-wiki
http://stackoverflow.com/a/32473678/1090562

Idea is the same as matching_books_names. Read it for an explanation.
This is just some alternative solution
"""

from nltk.corpus import stopwords
import string
from nltk.tokenize import wordpunct_tokenize as tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

n = input()
documents = [raw_input() for _ in xrange(n)]
raw_input()
documents +=[raw_input() for _ in xrange(n)]

def analyser(documents):
    porter = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    modified_arr = [[porter.stem(i.lower()) for i in tokenize(d.translate(None, string.punctuation)) if i.lower() not in stop_words] for d in documents]
    modified_doc = [' '.join(i) for i in modified_arr]

    tf_idf = TfidfVectorizer().fit_transform(modified_doc)

    for i in xrange(len(documents) / 2):
        minimum = (1, None)
        for j in xrange(len(documents) / 2, len(documents)):
            minimum = min((cosine(tf_idf[i].todense(), tf_idf[j].todense()), j - len(documents) / 2), minimum)
        print minimum[1] + 1


analyser(documents)

"""https://www.hackerrank.com/challenges/matching-book-names-and-descriptions
clean up all the data by removing bad characters and stop words. Use stemmer to trim the words

build vectorizer based on names and fit descriptions in it. Then find the smallest cosine distance
between a description and a name
This is my implementation. There is a better one
"""

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def analysis(names_original, descriptions_original):
    bad_chars, stemmer = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~0123456789', PorterStemmer()
    stop_words = set(stopwords.words('english') + ['st', 'nd', 'rd', 'th', 'paperback', 'edition'])
    f = lambda x: [stemmer.stem(i) for i in x.lower().translate(None, bad_chars).decode('utf-8').split() if i not in stop_words]

    names, descriptions = [' '.join(f(i)) for i in names_original], [' '.join(f(i)) for i in descriptions_original]

    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.2, analyzer='word')
    vectorizer.fit(names)

    names_array = np.array(vectorizer.transform(names).todense())
    descriptions_array = np.array(vectorizer.transform(descriptions).todense())

    # http://stackoverflow.com/q/32688866/1090562
    dots = np.dot(descriptions_array, names_array.T)
    l2norms = np.sqrt(((descriptions_array**2).sum(1)[:, None])*((names_array**2).sum(1)))
    cosine_dists = 1 - (dots / l2norms)
    cosine_dists[np.isnan(cosine_dists).all(1), 0] = 0
    return np.nanargmin(cosine_dists, axis=1)

n = input()
names_original = [raw_input() for i in xrange(n)]
raw_input()
descriptions_original = [raw_input() for i in xrange(n)]
for i in analysis(names_original, descriptions_original):
    print i + 1
# https://www.hackerrank.com/challenges/the-trigram
from nltk.util import ngrams
from collections import Counter

s = raw_input()
bad_chars = '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
s1 = s.encode('ascii', 'ignore').lower().translate(None, bad_chars).replace("\n", " ").replace("  ", " ").split()

res = Counter(ngrams(s1, 3))
print " ".join(res.most_common(1)[0][0])

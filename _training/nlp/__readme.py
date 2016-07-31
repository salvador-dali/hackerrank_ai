def readLinesFromFile(fname):
    # create a list of lines from the file
    bad_chars = '0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    return [line.rstrip('\n').translate(None, bad_chars) for line in open(fname)]

def readWordsFromFile(fname):
    # convert a file with lines to a long array of words
    return [word for line in open(fname) for word in line.decode('utf-8').encode('ascii', 'ignore').lower().translate(None, '.,?!;:&[]()*_"').split()]

def generatePotentialWordFromWordWithMissingSymbols(word):
    # Having a word with a missing symbol #, generates all the potential words
    from itertools import product

    c, word_arr, all_words = word.count('#'), list(word), []
    positions = [pos for pos, char in enumerate(word) if char == '#']

    for letters in product('abcdefghijklmnopqrstuvwxyz', repeat=c):
        for letter, pos in zip(letters, positions):
            word_arr[pos] = letter
        all_words.append(''.join(word_arr))

    return all_words

def compressDecompress(arr):
    # sometimes it is important to have your code handle more than 50kb limit
    # this shows how to compress the data (on your local machine) and decompress it
    import zlib, base64
    compressed = base64.b64encode(zlib.compress(' '.join(arr), 9))
    decompressed = [i for i in zlib.decompress(base64.b64decode(compressed)).split()]

def findSimilarities(text1, text2):
    """
    having two pairs of text (ideally equal size)
    find which sentence from text 1 corresponds two which in text 2
    """
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer  # from nltk.stem.snowball import SnowballStemmer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # you can try other stemmers: SnowballStemmer('english')
    bad_chars, stemmer = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~0123456789', PorterStemmer()
    stop_words = set(stopwords.words('english') + ['some', 'other', 'words'])

    # decode is only when there are non latin characters that should be ignored
    f = lambda x: [stemmer.stem(_) for _ in x.lower().translate(None, bad_chars).decode('utf-8').split() if _ not in stop_words]

    names, descr = [' '.join(f(i)) for i in text1], [' '.join(f(i)) for i in text2]
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.2, analyzer='word', ngram_range=(1, 2))
    arr = vectorizer.fit_transform(descr + names)

    # you can check for alternative without scikit in matching_books_names_my.py

    n = len(text1)
    # might be offset 1
    return [np.argmax(cosine_similarity(arr[i:i+1], arr)[0, n:]) + 1 for i in xrange(n)]

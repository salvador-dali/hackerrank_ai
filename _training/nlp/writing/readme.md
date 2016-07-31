[TF-IDF](http://en.wikipedia.org/wiki/Tf%E2%80%93idf)

which stands for term frequency, document frequency.
Shows how important is the word to a document in a collection of corpus.

**TF** - number of times the word appears in the document

**IDF** - logarithmically scaled fraction of the documents that contain the word, obtained by dividing the total number 
of documents by the number of documents containing a term. Diminish the weight of the super frequent words in the corpus.

Here we will try to find the ranking function which will tell how similar is the query *q* to the document *d*. This is *f(q, d)*.
In all the formulas we have the following conventions:

$\sum_{w \in q\cap d}$ - we sum over all the words which are exist in query and in the document

$c(w, D)$ - number of words $w$ in the document/query $D$

$M$ - total number of documents in the collection

$df(w)$ - document frequency. Number of documents that contains w.

$|d|$ - the length of the document $d$ in words.

$avdl$ - average document length in the text collection from which documents are drawn

$idf(w) = log\frac{M + 1}{df(w)}$ the way how inverse document frequency is calculated here (0)

##TF-IDF weighting##
$$f(q, d) = \sum_{w \in q\cap d} c(w, q) \cdot c(w,d) \cdot log\frac{M + 1}{df(w)}$$   (1)

The problem with this function is that we are not penalizing word that appears too much in the document. It linearly increase
the score, whereas we would like to make it less. We need something to avoid dominance by one single term over all others.
Hence the idea of TF transformation.

##BM25 transformation##
[BM25](http://en.wikipedia.org/wiki/Okapi_BM25) has the following transformation $\frac{(k+1)x}{x+k}$, where 
$k$ controls the upper bound $k + 1$. This upper bound is good (log does not have it). Also using different $k$ we can 
model different other transformation (check $k=0$ and $k=\infty $).

$$f(q, d) = \sum_{w \in q\cap d} c(w, q) \cdot \frac{(k+1)c(w,d)}{c(w,d)+k} \cdot log\frac{M + 1}{df(w)}$$ (2)
This is ranking function with BM25 TF.

Now we considered local statistics TF, global statistics IDF, but have not considered length of the document. 
The problem is that if we have very big document, it will have high chance of matching the query. So we need to penalize
it, by normalizing the document

## Pivoted length normalization ##
uses the following normalizer $1 - b + \frac{b|d|}{avdl}$, where $b \in [0, 1]$ and controls the length normalization 
if $b=0$ the normalizer is 1. if $b > 0$, the higher the $b$, the bigger we penalize long documents, and reward short one.

##State of the art ranking functions##

$$f(q, d) = \sum_{w \in q\cap d} c(w, q) \frac{ln(1 + ln(1 + c (w, d))))}{1 - b + \frac{b|d|}{avdl}}\cdot log\frac{M + 1}{df(w)}$$
pivoted length normalization

$$f(q, d) = \sum_{w \in q\cap d} c(w, q) \frac{(k + 1) c(w, d)}{c(w,d) + k(1 - b + \frac{b|d|}{avdl})}\cdot log\frac{M + 1}{df(w)}$$
$k \in [0, \infty )$

if will be implementing for competitions, check bm25+, it has better results.

Good reading
[Pivoted document length normalization](http://singhal.info/pivoted-dln.pdf), [Some simple effective approximations to the 2-Poisson model for probabilistic weighted retrieval](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.97.5858&rep=rep1&type=pdf)

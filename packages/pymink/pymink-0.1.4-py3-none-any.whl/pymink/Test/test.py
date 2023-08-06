from pymink._exceptions import PyMinkException
from pymink.cleaner import Cleaner
from pymink.ngram import word_ngrams
from pymink import DTXT_2

# create a cleaner
cleaner = Cleaner()

text = cleaner.clean(DTXT_2)

# create a ngram
ngram = word_ngrams(text, 3)

# print the ngram
print(ngram)
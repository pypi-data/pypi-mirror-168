from pymink import Cleaner
from pymink import DTXT_2
from pymink import word_ngrams, sentence_ngrams

cln = Cleaner()
filtered_text = cln.clean(DTXT_2)

df_word = word_ngrams(filtered_text, 2)
df_sentence = sentence_ngrams(filtered_text, 4)

print(df_word)

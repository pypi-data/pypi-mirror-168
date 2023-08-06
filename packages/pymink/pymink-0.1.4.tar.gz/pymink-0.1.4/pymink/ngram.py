"""
This module is used to generate all the ngrams from the filtered input text.
"""

from nltk import ngrams

import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict


def _get_dataframe_from_dict(ngram_dict: Dict) -> pd.DataFrame:
    """
    This function generates a dataframe from the ngram dictionary.

    This function is used internally by the word_ngrams and sentence_ngrams functions.
    """
    # Create df
    df = pd.DataFrame(ngram_dict.values(), columns=["Count"], index = pd.MultiIndex.from_tuples(ngram_dict.keys()))
    # Sort df
    df = df.sort_values(by="Count", ascending=False)
    # Add precentage collumn to df
    df["%"] = df["Count"] / df["Count"].sum() * 100

    return df


def word_ngrams(text: str, n: int, pad_symbol: str = "_") -> pd.DataFrame:
    """
    This function generates all the ngrams from the input text. The ngrams are generated from the words.
    """
    ngram_dict = {}

    for word in text.split():
        for gram in ngrams(word, n, pad_left=True, pad_right=True, left_pad_symbol=pad_symbol, right_pad_symbol=pad_symbol):
            ngram_dict[gram] = ngram_dict.get(gram, 0) + 1

    return _get_dataframe_from_dict(ngram_dict)


def sentence_ngrams(text: str, n: int, pad_symbol: str = "_") -> pd.DataFrame:
    """
    This function generates all the ngrams from the input text. The ngrams are generated from the sentences.
    """
    ngram_dict = {}
    
    for gram in ngrams(text.split(), n, pad_left=True, pad_right=True, left_pad_symbol=pad_symbol, right_pad_symbol=pad_symbol):
        ngram_dict[gram] = ngram_dict.get(gram, 0) + 1

    return _get_dataframe_from_dict(ngram_dict)

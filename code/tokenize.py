# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:05:03 2020

@author: kaima
"""

import keras.preprocessing.text
import nltk.corpus.reader.cmudict

file = open('../data/shakespeare.txt', 'r')
text = file.read()
word_sequence = keras.preprocessing.text.text_to_word_sequence(text, filters='0123456789!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
Tokenizer = keras.preprocessing.text.Tokenizer(num_words=None, filters='0123456789!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ', char_level=False, oov_token=None, document_count=0)
Tokenizer.fit_on_texts(word_sequence)
word_counts = Tokenizer.word_counts;
# print(word_counts)

print(Tokenizer)


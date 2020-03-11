# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 23:06:16 2020

@author: kaima
"""


import keras.preprocessing.text
import json

from HMM import unsupervised_HMM
from helper import (
    parse_poetry,
    format_poem
    )


# load file and read as text
file = open('../data/shakespeare.txt', 'r')
text = file.read()

# load syllable counter
with open('../data/word_to_syllable_dict.json') as f:
    w2s_dict = json.load(f)

# filter for Tokenizer
filters = '0123456789!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n' # get rid of '-'

word_sequence = keras.preprocessing.text.text_to_word_sequence(text, 
                                                               filters = filters,
                                                               lower = True,
                                                               split = ' ')

Tokenizer = keras.preprocessing.text.Tokenizer(num_words = None,
                                               filters = filters, 
                                               lower = True, 
                                               split = ' ', 
                                               char_level = False, 
                                               oov_token = None, 
                                               document_count = 0)

# fit Tokenizer
Tokenizer.fit_on_texts(word_sequence)

# convert text to observation (list of list of tokens) using Tokenizer
obs = parse_poetry(text,Tokenizer)


# %% Generate

# Generate a single input sequence of length M.
M = 200
ks = [6, 8, 10, 12, 14, 16, 18, 20]

for k in ks:
    
    # train the unsupervised HMM
    HMM = unsupervised_HMM(obs, k, 100)
    emission, _ = HMM.generate_emission(M)
    
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format("with k= "+str(k)))
    print("#" * 70)
    print('')
    print('')
    
    # generate a poem
    poem = format_poem(emission,Tokenizer,w2s_dict)
    for line in poem:
        print(line)
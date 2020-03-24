# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:44:05 2020

@author: kaima
"""

import keras.preprocessing.text
from helper import (parse_poetry, format_poem)
from HMM import unsupervised_HMM
import json

dataPath = '../data/'
# load file and read as text
file = open('../data/shakespeare.txt', 'r')
text = file.read()

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

# load syllable counter
with open(dataPath+'word_to_syllable_dict.json') as f:
    w2s_dict = json.load(f)


# fit Tokenizer
Tokenizer.fit_on_texts(word_sequence)

# convert text to observation (list of list of tokens) using Tokenizer
obs = parse_poetry(text,Tokenizer)

# train the unsupervised HMM
HMM = unsupervised_HMM(obs, 10, 100)



# %% 


MAX_WORDS = 20*14
emission, _ = HMM.generate_emission(MAX_WORDS)

poem = []
line = []
syllable_ctr = 0

for idx in emission:
    
    # convert token to the word
    # WARNING: Tokenizer is 1-indexed while HMM from HW6 is 0-indexed 
    word = Tokenizer.index_word[idx+1]
    line.append(word)
    
    # find the syllable count for the word
    syll_str = next(x for x in w2s_dict[word] if x.isdigit())
    syllable_ctr += int(syll_str)
    
    # stop when syllable count exceeds 10
    if syllable_ctr >= 10:
        poem.append(line)
        line = []
        syllable_ctr = 0
        if len(poem) == 14:
            break
        
poem_text = format_poem(poem) 
print(poem_text)


# save poems as text
fname_write = 'hmm_naive.txt'

with open(dataPath+fname_write, 'w') as f:
    f.write(poem_text)
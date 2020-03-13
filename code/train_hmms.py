# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 23:06:16 2020

@author: kaima
"""


import keras.preprocessing.text
import json
import random

from HMM import unsupervised_HMM
from helper import (
    parse_poetry_2,
    display_title,
    poem_that_rhymes,
    # format_poem
    )

dataPath = '../data/'

# load file and read as text
with open(dataPath+'shakespeare.txt', 'r') as f:
    text = f.read()

# load syllable counter
with open(dataPath+'word_to_syllable_dict.json') as f:
    w2s_dict = json.load(f)

with open(dataPath+'rhyme_to_word_dict.json') as f:
    r2w_dict = json.load(f)

with open(dataPath+'word_to_rhyme_dict.json') as f:
    w2r_dict = json.load(f)


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
obs = parse_poetry_2(text,Tokenizer)


# reverse the order so that prediction happens backwards (for Rhyme)
for line in obs:
    line.reverse()


# %% Generate

# ks = [6, 10, 14, 18, 22, 26, 30]
ks = [22, 26, 30]

for k in ks:
    
    display_title('k = '+str(k))
    
    # learn line-wise backwards HMM
    HMM = unsupervised_HMM(obs, k, 100)
    data = {}
    data['O'] = HMM.O
    data['A'] = HMM.A
    
    
    fname = 'OA_k'+str(k)+'.json'
    with open(dataPath+fname, 'w') as outfile:
        json.dump(data, outfile)
        
    # poem = poem_that_rhymes(HMM,Tokenizer,r2w_dict,w2s_dict)
    
    # print(poem)
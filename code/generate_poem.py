# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:45:59 2020

@author: kaima
"""

import keras.preprocessing.text
from HMM import HiddenMarkovModel
import json
from helper import poem_that_rhymes

dataPath = '../data/'

k = 26

fname = 'OA_k'+str(k)+'.json'


with open(dataPath+fname, 'r') as f:
    hmm_param = json.load(f)

# load file and read as text
with open(dataPath+'shakespeare.txt', 'r') as f:
    text = f.read()

# load syllable counter
with open(dataPath+'word_to_syllable_dict.json') as f:
    w2s_dict = json.load(f)

with open(dataPath+'rhyme_to_word_dict.json') as f:
    r2w_dict = json.load(f)


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

# initalize the 
HMM = HiddenMarkovModel(hmm_param['A'],hmm_param['O'])


poem_list = ""
for i in range(5):
    poem, syll_list = poem_that_rhymes(HMM,Tokenizer,r2w_dict,w2s_dict)
    poem_list += poem
    poem_list += "\n\n"
    for syll in syll_list:
        poem_list += str(syll) +', '
        
    poem_list += "\n\n"


# save poems as text
fname_write = 'hmm_poems_k' + str(k) + '.txt'

with open(dataPath+fname_write, 'w') as f:
    f.write(poem_list)

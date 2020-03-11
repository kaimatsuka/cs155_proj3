# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 23:06:16 2020

@author: kaima
"""


import keras.preprocessing.text
# import nltk.corpus.reader.cmudict
# import os
# import numpy as np
# from IPython.display import HTML


from HMM import unsupervised_HMM

def parse_poetry(text, Tokenizer):
    
    '''
    Convert text to an obsrevation that can be trained using HMM. The 
    observation is in form list of list of integers.
    '''
    # Convert text to dataset.
    lines = [line.split() for line in text.split('\n') if line.split()]
    
    # pre-allocate list of list
    obs = []
    poem_ctr = 0
    for line in lines:
        # print(line)
        if len(line) == 1:
    
            if poem_ctr != 0:
                obs.append(poem)
                
            poem_ctr += 1
            # re-initialize 
            poem = []
        else:
            for word in line:
                word = word.lower()
                word = word.replace('.\'','')    # edge case for poetry 50
                word = word.replace(',\'','')    # edge case for poetry 115
                word = word.replace(',', '')
                word = word.replace('.', '')
                word = word.replace(':', '')
                word = word.replace(';', '')
                word = word.replace('?', '')
                word = word.replace(')', '')
                word = word.replace('(', '')
                word = word.replace('!', '')
                poem.append(Tokenizer.word_index[word])
                
    # append the last poem
    obs.append(poem)
            
        
    return obs


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

# fit TOkenizer
Tokenizer.fit_on_texts(word_sequence)

# convert text to observation (list of list of tokens) using Tokenizer
obs = parse_poetry(text,Tokenizer)

# train the unsupervised HMM
hmm8 = unsupervised_HMM(obs, 10, 100)


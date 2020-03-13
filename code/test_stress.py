# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:44:51 2020

@author: kaima
"""


import json
import random

with open('../data/word_to_rhyme_dict.json') as f:
    w2r_dict = json.load(f)
with open('../data/rhyme_to_word_dict.json') as f:
    r2w_dict = json.load(f)
    


N_rhyme = 0
while N_rhyme < 3:
    random_key = random.choice(list(r2w_dict.keys()))
    N_rhyme = len(r2w_dict[random_key])
    print(r2w_dict[random_key])
    
print(r2w_dict[random_key])
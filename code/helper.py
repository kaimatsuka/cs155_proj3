# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:40:17 2020

@author: kaima
"""


import random
import numpy as np

def parse_poetry(text, Tokenizer):
    
    '''
    Convert input text to an obsrevation that can be trained using HMM.  
    The observation is in form list of list of integers.
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

def parse_poetry_2(text, Tokenizer):
    
    '''
    Convert text to an obsrevation that can be trained using HMM. The 
    observation is in form list of list of integers.
    '''
    # Convert text to dataset.
    lines = [line.split() for line in text.split('\n') if line.split()]
    
    # pre-allocate list of list
    obs = []
    poem_ctr = 0
    line = 0
    lineToken = []
    for line in lines:
        # print(line)
        if len(line) == 1:
    
            continue
    
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
            
            # MINUS 1 because Tokenizer is 1-indexed, while the
            # HMM from HW6 is 0-indexed!!
            lineToken.append(Tokenizer.word_index[word]-1)
        
        obs.append(lineToken)
        lineToken = []
        
    return obs


def display_title(title_str):
                  
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format(title_str))
    print("#" * 70)
    print('')
    print('')
    pass

def format_poem(poem_words):
    
    '''
    This function takes a generated poem (list of list of words) and formats
    into a readable form.
    poetry_words

    Input:
        poem_words:     list of list of words, such that len(poem_words) = 14
                        and peom_words[0][0] denote the first word in the poem
    '''
    
    N_lines = len(poem_words)
    
    poem_text = ""
    
    # visit each line in a poem
    for currLine, line in enumerate(poem_words):
    
        N_words = len(line) # number of words in that line
        
        # visit each word in a line
        for curr, word in enumerate(line):
            
            
            if word is "i":
                word = "I"
                
            # capitalize the first word of each line
            if curr == 0:
                word = word.capitalize()
                
            # For the last word in line
            if curr == (N_words-1):
                
                # if this is the last word of poem, add period and 
                if currLine == (N_lines-1):
                    poem_text += word + "."
                    break
                
                # otherwise, add comma and new line
                poem_text += word + ",\n"
                
            else:
                # for non-last words, add space
                poem_text += word + " "
                
    return poem_text

def get_ten_syllable(emission,Tokenizer,w2s_dict):

    '''
    Get a line with ten syllable count.
    
    Note: Sometimes syllable dictionary contains edge cases. for example
            'flatter': ['E1', '2']
            'being': ['1', '2']
          Find the first syllable count that's not of format 'E?' then add it
    Returns:
        words:  list of strings
    ''' 
    
    words = []
    syllable_ctr = 0
    # print(emission)
    for idx in emission:
        
        # convert token to the word
        # WARNING: Tokenizer is 1-indexed while HMM from HW6 is 0-indexed 
        word = Tokenizer.index_word[idx+1]
        words.append(word)
        
        # find the syllable count for the word
        syll_str = next(x for x in w2s_dict[word] if x.isdigit())
        syllable_ctr += int(syll_str)
        
        # stop when syllable count exceeds 10
        if syllable_ctr >= 10:
            break

    return words

def sample_rhymeKey(r2w_dict):
    '''
    Randomly select a rhyme key, such that the key has at least 3 words 
    to pick from.
    '''
    
    N_rhyme = 0
    while N_rhyme < 3:
        random_key = random.choice(list(r2w_dict.keys()))
        N_rhyme = len(r2w_dict[random_key])
        
    return random_key


def lines_that_rhymes(HMM, Tokenizer, r2w_dict, w2s_dict):
    
    # randomly rhyme key such that that key has at least 3 words to pick from
    rhyme_key = sample_rhymeKey(r2w_dict)
    # print(rhyme_key)
    # select two words without replacement
    rhyme_pair = np.random.choice(r2w_dict[rhyme_key],2,replace=False)
    # print(rhyme_pair)
    
    MAX_WORDS = 20
    lines = []
    for seed in rhyme_pair:
        seed_idx = Tokenizer.word_index[seed]-1
        emission, _ = HMM.generate_emission_with_seed(MAX_WORDS,seed_idx)
        # print(emission)
        line_backward = get_ten_syllable(emission,Tokenizer,w2s_dict)
        # print(line_backward)
        line_backward.reverse()
        lines.append(line_backward)
        
    return lines
        
def poem_that_rhymes(HMM_back,Tokenizer,r2w_dict,w2s_dict):
    
    
    lines_a = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    lines_b = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    lines_c = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    lines_d = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    lines_e = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    lines_f = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    lines_g = lines_that_rhymes(HMM_back, Tokenizer, r2w_dict, w2s_dict)
    
    # construct a poetry with rhymes (as list of list of token)
    poem_words = [lines_a[0], lines_b[0], lines_a[1], lines_b[1],
              lines_c[0], lines_d[0], lines_c[1], lines_d[1],
              lines_e[0], lines_f[0], lines_e[1], lines_f[1],
              lines_g[0], lines_g[1]]
    
    
    # get syllable count for each line
    
    syll_list = []
    for line in poem_words:
        syllable_ctr = 0
        for word in line:
            
            # find the syllable count for the word
            syll_str = next(x for x in w2s_dict[word] if x.isdigit())
            syllable_ctr += int(syll_str)
        syll_list.append(syllable_ctr)
    
    # foramt poem for capitalization, space, punctuation,etc
    poem_text = format_poem(poem_words)

    return poem_text, syll_list
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:40:17 2020

@author: kaima
"""



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


def display_title(title_str):
                  
    print('')
    print('')
    print("#" * 70)
    print("{:^70}".format(title_str))
    print("#" * 70)
    print('')
    print('')
    pass

def format_poem(emission,Tokenizer,w2s_dict):
    
    # create a poem
    syllable_ctr = 0
    line_ctr = 0
    line = ''
    poetry = []
    
    for idx in emission:
        
        # get a word
        word = Tokenizer.index_word[idx]
        
        # add word to this line. Capitalize the first letter for style
        if syllable_ctr == 0:
            line += word.capitalize()
        else:
            line += word
    
        
        # increment syllable with syllable count
        # as a by product of json file, dictionary maps to a list
        # sometimes syllable dictionary contains edge cases. for example
        # 'flatter': ['E1', '2']
        # 'being': ['1', '2']
        # find the first syllable count that's not of format 'E?' 
        # then add it to counter
        syll_str = next(x for x in w2s_dict[word] if x.isdigit())
        syllable_ctr += int(syll_str)
        
        # next line if the syllable count for this line is 10 or larger
        if syllable_ctr >= 10:
    
            # add comma at the end of line (and period at the end of poem) 
            # for style purpose
            if line_ctr == 13:
                line += '.'
            else:
                line += ','
            
            # add line
            poetry.append(line)
            line_ctr += 1
            
            # re-initalize the line and syllable counter
            line = ''
            syllable_ctr = 0
            
            # finish if this is last line of the poem
            if line_ctr == 14:
                break
            
        else:
            line += ' '
            
    
    return poetry

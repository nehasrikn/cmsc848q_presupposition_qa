from distutils.util import change_root
import json 
import spacy 


continuation_of_state_filepath = "./wordlists/continuation_of_state_predicates.txt"

def find_continuation_of_state(sentence, continuation_of_state_predicates=continuation_of_state_filepath):
    with open(continuation_of_state_predicates) as f: 
        continuation_of_state_predicates = set([l.strip() for l in f.readlines()]) 


    words = [t.text for t in sentence]
    
    if set(words) & continuation_of_state_predicates: 
        for token in sentence: 
            if (str(token)) in continuation_of_state_predicates and token.tag_[0] == "V" and token.dep_ == "ROOT": 
                
                for child in token.children: 
                    if child.dep_ in ["xcomp", "ccomp"]: 

                        return True 


    return False 

    